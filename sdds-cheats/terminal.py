"""Clientes de terminal para o serviço local Sdds cheats."""
import argparse
import getpass
import http.cookiejar
import json
import urllib.error
import urllib.request


class Client:
    def __init__(self, base):
        self.base = base.rstrip('/')
        self.http = urllib.request.build_opener(
            urllib.request.ProxyHandler({}),
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def call(self, path, data=None):
        body = json.dumps(data).encode() if data is not None else None
        request = urllib.request.Request(self.base + '/api/' + path, data=body,
                                         headers={'Content-Type': 'application/json'})
        try:
            with self.http.open(request, timeout=15) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            try:
                message = json.load(exc).get('error', 'Operação recusada.')
            except (ValueError, AttributeError):
                message = 'Operação recusada.'
            raise ValueError(message) from None


def credentials():
    return {'name': input('Usuário: ').strip(), 'password': getpass.getpass('Senha: ')}


def show_subscription(state):
    from datetime import datetime
    print('Assinatura:', 'ATIVA' if state['active'] else 'INATIVA')
    if state['expires_utc_unix']:
        expiry = datetime.fromtimestamp(state['expires_utc_unix']).astimezone()
        print('Vencimento:', expiry.strftime('%d/%m/%Y %H:%M:%S %z'))


def run(client, admin=False):
    print('\n=== SDDS CHEATS — ' + ('ADMIN' if admin else 'USUÁRIO') + ' ===')
    if not admin and input('Já tem conta? [S/n]: ').strip().lower() == 'n':
        client.call('register', credentials())
        print('Conta criada. Entre abaixo.')
    client.call('login', credentials())
    try:
        state = client.call('me')
        if admin:
            if not state['admin']:
                raise ValueError('Esta conta não é administradora.')
            while True:
                print('\n1 — Gerar key | 2 — Listar keys | 3 — Revogar | 0 — Sair')
                option = input('Escolha: ').strip()
                if option == '0':
                    return
                try:
                    if option == '1':
                        days = int(input('Duração [30 ou 60 dias]: '))
                        if days not in (30, 60):
                            raise ValueError('Escolha 30 ou 60 dias.')
                        result = client.call('admin/keys', {'days': days})
                        print('ID:', result['id'], '| Dias:', result['days'])
                        print('KEY:', result['key'])
                        print('Guarde a key: ela não será mostrada na listagem.')
                    elif option == '2':
                        rows = client.call('admin/keys')
                        if not rows:
                            print('Nenhuma key cadastrada.')
                        for row in rows:
                            status = 'REVOGADA' if row['revoked'] else ('ATIVADA' if row['user_id'] else 'DISPONÍVEL')
                            print(f"ID {row['id']} | {row['days']} dias | {status} | Usuário ID: {row['user_id']}")
                    elif option == '3':
                        kid = int(input('ID da key: '))
                        print('Isso encerra toda a assinatura e as sessões do titular.')
                        if input('Digite REVOGAR para confirmar: ').strip() == 'REVOGAR':
                            print(client.call('admin/revoke', {'id': kid})['status'])
                    else:
                        print('Opção inválida.')
                except ValueError as exc:
                    print('Erro:', exc)
        else:
            show_subscription(state)
            key = getpass.getpass('Key de assinatura (Enter para apenas consultar): ').strip()
            if key:
                client.call('activate', {'key': key})
                print('Key ativada.')
                state = client.call('me')
                show_subscription(state)
            if state['active']:
                print('Acesso à assinatura validado. O cliente do jogo ainda não está integrado.')
            else:
                print('É necessário ativar uma key válida para obter uma assinatura.')
    finally:
        try:
            client.call('logout', {})
        except (OSError, ValueError):
            pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--admin', action='store_true')
    args = parser.parse_args()
    try:
        client = Client('http://127.0.0.1:8085')
        if args.admin:
            run(client, True)
        else:
            print('\n=== SDDS CHEATS ===')
            key = getpass.getpass('Digite sua key: ').strip()
            state = client.call('license', {'key': key})
            show_subscription(state)
            print('\nInicie o Combat Arms Brazil ou Engine.exe')
            print('Este programa valida a licença. Não inclui DLL nem injeta no jogo.')
        return 0
    except (EOFError, KeyboardInterrupt):
        print('\nEncerrado.')
        return 0
    except ValueError as exc:
        print('Erro:', exc)
        return 1
    except (OSError, urllib.error.URLError):
        print('Não foi possível conectar. Inicie start.bat e mantenha o servidor aberto.')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
