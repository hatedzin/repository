import argparse
import getpass
import hashlib
import hmac
import secrets
import sqlite3
import time
from pathlib import Path

from aiohttp import web

ROOT = Path(__file__).resolve().parent


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def password_hash(password, salt=None):
    if len(password) < 12:
        raise ValueError('A senha precisa ter pelo menos 12 caracteres.')
    salt = salt or secrets.token_hex(16)
    return salt + ':' + hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt), n=16384, r=8, p=1).hex()


class Store:
    def __init__(self, path):
        path = Path(path)
        fresh = not path.exists()
        self.db = sqlite3.connect(path)
        if fresh:
            path.chmod(0o600)
        self.db.row_factory = sqlite3.Row
        self.db.execute('PRAGMA foreign_keys=ON')
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL,
          password TEXT NOT NULL, admin INTEGER NOT NULL DEFAULT 0, expires REAL NOT NULL DEFAULT 0);
        CREATE TABLE IF NOT EXISTS licenses(id INTEGER PRIMARY KEY, hash TEXT UNIQUE NOT NULL,
          days INTEGER NOT NULL CHECK(days IN (30,60)), user_id INTEGER REFERENCES users(id), revoked INTEGER NOT NULL DEFAULT 0);
        CREATE TABLE IF NOT EXISTS sessions(hash TEXT PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id), expires REAL NOT NULL);
        ''')

    def user(self, name, password, admin=False):
        if not 3 <= len(name) <= 64:
            raise ValueError('Nome deve ter entre 3 e 64 caracteres.')
        with self.db:
            self.db.execute('INSERT INTO users(name,password,admin) VALUES(?,?,?)', (name, password_hash(password), int(admin)))

    def issue(self, days):
        if days not in (30, 60):
            raise ValueError('Escolha 30 ou 60 dias.')
        key = 'SDDS-' + secrets.token_urlsafe(24)
        with self.db:
            cursor = self.db.execute('INSERT INTO licenses(hash,days) VALUES(?,?)', (digest(key), days))
        return {'id': cursor.lastrowid, 'key': key, 'days': days}

    def activate(self, uid, key):
        with self.db:
            row = self.db.execute('SELECT * FROM licenses WHERE hash=?', (digest(key),)).fetchone()
            if not row or row['revoked'] or row['user_id'] is not None:
                raise ValueError('Key inválida, revogada ou já utilizada.')
            old = self.db.execute('SELECT expires FROM users WHERE id=?', (uid,)).fetchone()[0]
            expiry = max(old, time.time()) + row['days'] * 86400
            self.db.execute('UPDATE licenses SET user_id=? WHERE id=?', (uid, row['id']))
            self.db.execute('UPDATE users SET expires=? WHERE id=?', (expiry, uid))
        return expiry


PAGE = (ROOT / 'panel.html').read_text(encoding='utf-8')


def create_app(store, secure=False):
    attempts = {}

    @web.middleware
    async def errors(request, handler):
        if request.method == 'POST':
            # Browsers must send JSON and same-origin requests.
            origin = request.headers.get('Origin')
            if request.content_type != 'application/json' or (origin and origin != f'{request.scheme}://{request.host}'):
                return web.json_response({'error': 'Origem ou formato inválido.'}, status=403)
        try:
            return await handler(request)
        except (ValueError, KeyError, TypeError, sqlite3.IntegrityError):
            return web.json_response({'error': 'Dados inválidos, conta existente ou key indisponível.'}, status=400)

    def current(request, admin=False):
        row = store.db.execute('SELECT u.* FROM users u JOIN sessions s ON s.user_id=u.id WHERE s.hash=? AND s.expires>?', (digest(request.cookies.get('session', '')), time.time())).fetchone()
        if not row:
            raise web.HTTPUnauthorized(text='{"error":"Entre na sua conta."}', content_type='application/json')
        if admin and not row['admin']:
            raise web.HTTPForbidden(text='{"error":"Administrador necessário."}', content_type='application/json')
        return row

    async def api(request):
        action = request.match_info['action']
        data = await request.json() if request.method == 'POST' else {}
        if action in ('register', 'login') and request.method == 'POST':
            ip = request.remote
            now = time.time()
            if len(attempts) > 10000:
                for k in list(attempts):
                    if attempts[k][0] < now - 600:
                        del attempts[k]
            start, count = attempts.get(ip, (now, 0))
            if now - start > 600:
                start, count = now, 0
            attempts[ip] = (start, count + 1)
            if count >= 15:
                return web.json_response({'error': 'Tente novamente em 10 minutos.'}, status=429)
            name, password = data['name'], data['password']
            if not isinstance(name, str) or not isinstance(password, str) or len(password) > 256:
                raise ValueError()
            if action == 'register':
                store.user(name, password)
                return web.json_response({'status': 'Conta criada. Faça login.'}, status=201)
            row = store.db.execute('SELECT * FROM users WHERE name=?', (name,)).fetchone()
            expected = row['password'] if row else password_hash('dummy-password-for-timing', '00' * 16)
            if not hmac.compare_digest(password_hash(password, expected.split(':')[0]), expected) or not row:
                return web.json_response({'error': 'Usuário ou senha inválidos.'}, status=401)
            token = secrets.token_urlsafe(32)
            with store.db:
                store.db.execute('DELETE FROM sessions WHERE expires<?', (time.time(),))
                store.db.execute('INSERT INTO sessions VALUES(?,?,?)', (digest(token), row['id'], time.time() + 28800))
            response = web.json_response({'status': 'Login realizado.'})
            response.set_cookie('session', token, httponly=True, secure=secure, samesite='Strict', max_age=28800)
            return response
        user = current(request, action.startswith('admin/'))
        if action == 'me' and request.method == 'GET':
            return web.json_response({'name': user['name'], 'admin': bool(user['admin']), 'active': user['expires'] > time.time(), 'expires_utc_unix': user['expires']})
        if action == 'logout' and request.method == 'POST':
            with store.db:
                store.db.execute('DELETE FROM sessions WHERE hash=?', (digest(request.cookies.get('session', '')),))
            response = web.json_response({'status': 'Sessão encerrada.'})
            response.del_cookie('session')
            return response
        if action == 'activate' and request.method == 'POST':
            return web.json_response({'expires_utc_unix': store.activate(user['id'], data['key'])})
        if action == 'admin/keys':
            if request.method == 'POST':
                return web.json_response(store.issue(data['days']), status=201)
            return web.json_response([dict(r) for r in store.db.execute('SELECT id,days,user_id,revoked FROM licenses ORDER BY id DESC LIMIT 200')])
        if action == 'admin/revoke' and request.method == 'POST':
            with store.db:
                row = store.db.execute('SELECT user_id FROM licenses WHERE id=?', (data['id'],)).fetchone()
                if not row:
                    raise ValueError()
                store.db.execute('UPDATE licenses SET revoked=1 WHERE id=?', (data['id'],))
                if row['user_id']:
                    store.db.execute('UPDATE users SET expires=0 WHERE id=?', (row['user_id'],))
                    store.db.execute('DELETE FROM sessions WHERE user_id=?', (row['user_id'],))
            return web.json_response({'status': 'Key revogada; assinatura e sessões do titular encerradas.'})
        raise web.HTTPNotFound()

    app = web.Application(middlewares=[errors], client_max_size=4096)
    async def index(request):
        return web.Response(text=PAGE, content_type='text/html', headers={'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff'})
    app.router.add_get('/', index)
    app.router.add_get('/api/{action:.*}', api)
    app.router.add_post('/api/{action:.*}', api)
    return app


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', default=str(ROOT / 'sdds.sqlite3'))
    parser.add_argument('--create-admin', metavar='USUARIO')
    parser.add_argument('--port', type=int, default=8085)
    parser.add_argument('--secure-cookies', action='store_true')
    args = parser.parse_args()
    store = Store(args.db)
    if args.create_admin:
        password = getpass.getpass('Senha do administrador: ')
        if password != getpass.getpass('Repita a senha: '):
            raise SystemExit('As senhas não conferem.')
        store.user(args.create_admin, password, admin=True)
        print('Administrador criado.')
    else:
        web.run_app(create_app(store, args.secure_cookies), host='127.0.0.1', port=args.port, access_log=None)
