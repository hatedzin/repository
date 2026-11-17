# ASTRO — site de contas e painel GM/ADM

Implementado no ZIP enviado para esta solicitação, sem reaproveitar as alterações anteriores do menu SWF.

- Site preto/grafite/vermelho, ícones SVG e layout responsivo, com páginas de cadastro, login, recuperação, perfil, licenças e sessões.
- Contas USER/GM/ADM persistidas no MySQL existente. Conta GM solicitada criada automaticamente uma única vez, em Argon2id, ativa, com troca de senha obrigatória. Sem credenciais iniciais no frontend ou nos logs.
- Geração e entrega de keys aleatórias, consulta pelo titular, validade temporária/permanente, limites, redefinição de dispositivos, renovação, bloqueio, revogação e transferência com troca do código.
- Painel de usuários, pesquisa, histórico e estatísticas reais. Somente ADM altera cargos; o último ADM ativo é protegido. O primeiro ADM é provisionado por CLI local do dono da instalação, sem uma conta administrativa escondida.
- Integração com a autenticação real por key do client. Usuários antigos podem ser vinculados pelo dono da instalação, preservando dados e licenças. Novos cadastros não podem reivindicar identidades legadas.
- Sessões com tokens opacos, cookies HttpOnly/SameSite, proteção CSRF, SQL parametrizado, renderização segura e limitação de tentativas persistida no banco. Códigos das keys são criptografados; senhas e tokens de autenticação não são armazenados em texto puro.
- Ferramentas do client restauradas: configuração, upload/exportação e remoção de mapas Soft pelo backend original. SWF, robô, ActionScript e parser mantidos por comparação de hashes.
- `INICIAR_SITE.bat` abre o site sem esperar o parser do jogo. `INICIAR_CLIENT.bat` mantém o fluxo completo do client.

## Validação

Executados testes de integração com MariaDB 11.8 real, requisições HTTP e SMTP local: migração com dados existentes, seed idempotente, Argon2id, mudança obrigatória, permissões, isolamento entre usuários, geração/distribuição, limites, bloqueio, revogação, transferência, compatibilidade `/auth`, sessões, recuperação expirada/uso único e concorrência, CSRF e pesquisa com tentativa de SQL Injection.

Chromium passou em 14 verificações dos fluxos desktop/celular e 8 de ADM/XSS/ferramentas. Um roteiro adicional confirmou recuperação de senha com sessão já aberta. O iniciador do site foi exercitado com backend real e parser ausente. Logs, scripts e capturas acompanham o pacote.

A recuperação por email precisa de SMTP real preenchido no `.env`; foi testado o protocolo com um capturador local, sem enviar mensagens externas. Não houve implantação pública nem execução no Windows/Flash. Os limites de conexão referem-se a autorizações vigentes do backend, não a sockets do jogo oficial; não foi adicionado um mecanismo de expulsão ao SWF.

## Instalação

Extraia tudo, abra `PREPARAR_PASTA.bat`, configure o MySQL em `DisneyClient/.env` e execute `INICIAR_SITE.bat`. A conta `gmaccount` será criada no primeiro início com a senha inicial solicitada e exigirá a troca antes do gerenciamento. Leia `PORTAL-INSTALACAO.md` para SMTP, primeiro ADM, vínculo de usuários legados e backups.

Em atualizações, preserve banco, `.env` e `DisneyClient/.private/portal.key`. Nenhum segredo da instância de testes está no pacote.
