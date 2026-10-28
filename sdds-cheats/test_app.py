import tempfile
import time
import unittest
import asyncio
import contextlib
import io
from unittest.mock import patch
from pathlib import Path
from aiohttp.test_utils import TestClient, TestServer
from app import Store, create_app
from terminal import Client, run


class AuthTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.temp.name) / 'test.sqlite3')
        self.store.user('admin', 'temporary-admin-password', True)
        self.admin = TestClient(TestServer(create_app(self.store)))
        self.user = TestClient(TestServer(create_app(self.store)))
        await self.admin.start_server()
        await self.user.start_server()

    async def asyncTearDown(self):
        await self.admin.close()
        await self.user.close()
        self.store.db.close()
        self.temp.cleanup()

    async def test_complete_subscription_flow(self):
        r = await self.user.post('/api/admin/keys', json={'days': 30})
        self.assertEqual(r.status, 401)
        r = await self.admin.post('/api/login', json={'name':'admin','password':'temporary-admin-password'})
        self.assertEqual(r.status, 200)
        r = await self.user.post('/api/register', json={'name':'player','password':'temporary-player-password','admin':True})
        self.assertEqual(r.status, 201)
        r = await self.user.post('/api/login', json={'name':'player','password':'wrong-password'})
        self.assertEqual(r.status, 401)
        r = await self.user.post('/api/login', json={'name':'player','password':'123'})
        self.assertEqual(r.status, 401)
        self.assertEqual((await r.json())['error'], 'Usuário ou senha inválidos.')
        r = await self.user.post('/api/login', json={'name':'missing','password':''})
        self.assertEqual(r.status, 401)
        await self.user.post('/api/login', json={'name':'player','password':'temporary-player-password'})
        r = await self.user.post('/api/admin/keys', json={'days':30})
        self.assertEqual(r.status, 403)
        r = await self.admin.post('/api/admin/keys', json={'days':90})
        self.assertEqual(r.status, 400)
        for days in (30,60):
            r = await self.admin.post('/api/admin/keys', json={'days':days})
            self.assertEqual(r.status, 201)
            issued = await r.json()
            r = await self.user.post('/api/activate', json={'key':issued['key']})
            self.assertEqual(r.status, 200)
            r = await self.user.post('/api/activate', json={'key':issued['key']})
            self.assertEqual(r.status, 400)
        state = await (await self.user.get('/api/me')).json()
        self.assertTrue(state['active'])
        self.assertFalse(state['admin'])
        self.assertAlmostEqual(state['expires_utc_unix']-time.time(),90*86400,delta=10)
        with self.store.db:
            self.store.db.execute('UPDATE users SET expires=? WHERE name=?',(time.time()-1,'player'))
        state = await (await self.user.get('/api/me')).json()
        self.assertFalse(state['active'])
        r = await self.admin.post('/api/admin/revoke',json={'id':issued['id']})
        self.assertEqual(r.status,200)
        self.assertEqual((await self.user.get('/api/me')).status,401)
        r = await self.admin.get('/api/admin/keys')
        self.assertNotIn('hash',await r.text())

    async def test_browser_origin_and_logout(self):
        r = await self.admin.post('/api/login',json={'name':'admin','password':'temporary-admin-password'},headers={'Origin':'https://other.example'})
        self.assertEqual(r.status,403)
        await self.admin.post('/api/login',json={'name':'admin','password':'temporary-admin-password'})
        self.assertEqual((await self.admin.get('/')).status,200)
        self.assertEqual((await self.admin.post('/api/logout',json={})).status,200)
        self.assertEqual((await self.admin.get('/api/me')).status,401)

    async def test_terminal_clients(self):
        base = str(self.admin.make_url('/')).rstrip('/')
        output = io.StringIO()
        def admin_flow():
            with patch('builtins.input', side_effect=['admin','1','30','2','0']), patch('getpass.getpass', return_value='temporary-admin-password'), contextlib.redirect_stdout(output):
                run(Client(base), admin=True)
        await asyncio.to_thread(admin_flow)
        self.assertIn('KEY: SDDS-', output.getvalue())
        self.assertIn('DISPONÍVEL', output.getvalue())
        self.store.user('terminal-user','temporary-user-password')
        issued = self.store.issue(60)
        output = io.StringIO()
        def user_flow():
            with patch('builtins.input', side_effect=['s','terminal-user']), patch('getpass.getpass', side_effect=['temporary-user-password',issued['key']]), contextlib.redirect_stdout(output):
                run(Client(base))
        await asyncio.to_thread(user_flow)
        self.assertIn('Key ativada.',output.getvalue())
        self.assertIn('Assinatura: ATIVA',output.getvalue())
        self.assertEqual(self.store.db.execute('SELECT count(*) FROM sessions').fetchone()[0],0)

    async def test_key_only_login(self):
        key = self.store.issue(30)
        first = await self.user.post('/api/license', json={'key':key['key']})
        self.assertEqual(first.status,200)
        expiry = (await first.json())['expires_utc_unix']
        second = await self.user.post('/api/license', json={'key':key['key']})
        self.assertEqual((await second.json())['expires_utc_unix'],expiry)
        bad = await self.user.post('/api/license',json={'key':'SDDS-'+'wrong'*6})
        self.assertEqual(bad.status,401)
        with self.store.db:
            self.store.db.execute('UPDATE users SET expires=0 WHERE id=(SELECT user_id FROM licenses WHERE id=?)',(key['id'],))
        expired = await self.user.post('/api/license',json={'key':key['key']})
        self.assertEqual(expired.status,403)
        with self.store.db:
            self.store.db.execute('UPDATE licenses SET revoked=1 WHERE id=?',(key['id'],))
        revoked = await self.user.post('/api/license',json={'key':key['key']})
        self.assertEqual(revoked.status,401)

    async def test_default_key_persists_without_reset(self):
        first = await self.user.post('/api/license',json={'key':'sddskey'})
        self.assertEqual(first.status,200)
        expiry = (await first.json())['expires_utc_unix']
        reopened = Store(Path(self.temp.name) / 'test.sqlite3')
        reopened.db.close()
        second = await self.user.post('/api/license',json={'key':'sddskey'})
        self.assertEqual((await second.json())['expires_utc_unix'],expiry)
        from app import digest
        row = self.store.db.execute('SELECT u.admin FROM users u JOIN licenses l ON l.user_id=u.id WHERE l.hash=?',(digest('sddskey'),)).fetchone()
        self.assertEqual(row[0],0)
        with self.store.db:
            self.store.db.execute('UPDATE licenses SET revoked=1 WHERE hash=?',(digest('sddskey'),))
        reopened = Store(Path(self.temp.name) / 'test.sqlite3')
        reopened.db.close()
        self.assertEqual((await self.user.post('/api/license',json={'key':'sddskey'})).status,401)


if __name__ == '__main__':
    unittest.main()
