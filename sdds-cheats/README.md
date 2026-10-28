# Sdds cheats — contas e licenças

Serviço independente de login com painel web local, administrador e keys de
30 ou 60 dias. Não contém cliente de jogo nem integração com BattlEye.
O ZIP recebido contém oito arquivos de texto, sem projeto compilável.
“VALOFE 2026” não identifica uma build exata para validar offsets.

## Executar

Requer Python 3.11 ou superior. O painel tem tema escuro, menu lateral,
interruptores e sliders inspirados na referência. Os controles da aba Visual
são demonstrações; as abas Conta e Admin usam o serviço real.

No Windows, execute no terminal da pasta extraída:

```bat
start.bat --create-admin admin
start.bat
```

No Linux, é possível usar `bash start.sh --create-admin admin` e depois
`bash start.sh`. O inicializador instala dependências na primeira execução.
O inicializador Windows foi incluído, mas não foi executado neste ambiente Linux.

### Terminal Windows (CMD)

1. Crie o administrador uma única vez: `start.bat --create-admin admin`.
2. Inicie `start.bat` e mantenha essa janela aberta (servidor).
3. Abra `admin.cmd` para entrar como administrador e gerar, listar ou revogar keys.
4. Abra `usuario.cmd` para criar conta, entrar e informar a key de assinatura.

Os dois clientes usam o serviço local na porta 8085 e o mesmo banco do painel.
O usuário informa conta, senha e key; não há login somente por key.
Senhas e keys digitadas pelo usuário não aparecem no terminal.
Uma assinatura ativa valida o acesso ao serviço de licenças; não inicia um jogo.
Os arquivos CMD exigem Windows e não foram executados no ambiente Linux.

Instalação manual:

```sh
cd /workspace/sdds-cheats
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python app.py --create-admin admin
.venv/bin/python app.py
```

Abra a porta local 8085 no seu próprio ambiente. Faça login como administrador
e gere uma key de 30 ou 60 dias. Ela é mostrada somente na criação; guarde-a
para entregar ao usuário. O usuário cria conta, entra e ativa a key.
O prazo começa na ativação. Renovações somam dias ao período ainda válido.
Cada key só pode ser usada uma vez. Revogar uma key encerra toda a assinatura
e todas as sessões do titular, inclusive quando ele ativou outras keys.

Senhas usam scrypt; keys e tokens de sessão são armazenados como hashes.
Sessões duram oito horas. `/api/me` informa `active` e o vencimento Unix UTC.
Clientes autorizados precisam consultar a validade no servidor para liberar
funcionalidades; este projeto ainda não implementa essa integração.

O banco SQLite fica em `sdds.sqlite3`. Preserve-o em backups privados.
Não existe senha padrão nem administrador criado automaticamente.
Não envie o banco ou credenciais ao Git. Para produção, configure HTTPS,
use `--secure-cookies` e um proxy de confiança, revise proteção contra abuso
e a política de backups. O limitador atual é por IP e por processo.

## Validação

```sh
.venv/bin/python -m unittest -v test_app.py
```

Os testes usam banco temporário e exercitam HTTP real local: login,
permissões, ativação única, planos, expiração, revogação, origem e logout.
