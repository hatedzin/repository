# ASTRO MENU RGB V2 — correção do erro #1009

A V1 tentava construir a interface nativa ao carregar o jogo, ainda na tela de login. O teste de regressão reproduziu a mesma mensagem da captura enviada: “Falha ao abrir o menu: Error #1009”.

A V2 usa a interface criada pelo próprio jogo e verifica se seus controles e Keys estão prontos. Ao clicar antes do login, aparece “Entre no jogo para abrir o menu”; o pedido fica pendente e abre quando a interface fica pronta. Interface parcial também aguarda. Fechar/reabrir reutiliza o painel, sem abertura repetida pelo observador.

A correção se limita à inicialização do menu em AstroMenuShell. RGB, Inter e arte mantidos. Nenhum método do robô, Follow, gravação, rotas, entrada nativa ou Statements foi alterado. Backend/parser e configurações mantidos.

## Validação

- Regressão reproduzida na V1: #1009 na abertura sem interface nativa.
- V2: 15 testes de login/abertura do menu aprovados.
- V2: 32 testes de interface/RGB aprovados.
- Verificador estrutural: 1.597 métodos originais idênticos; métodos de Robot/Follow/REC/entrada nativa/Statements intactos; 87 corpos de apresentação verificados.
- Fontes Inter incorporadas e arte preservadas.
- Testes executados em Ruffle com objetos simulados. Ainda não validado em Adobe Flash/Windows nem em sessão real do jogo.

## Instalação

Feche o Flash e o client anterior. Extraia o ZIP completo em outra pasta, abra PREPARAR_PASTA.bat e copie sua .env anterior para DisneyClient-Local-Robot-Novo/DisneyClient/.env, se necessário. Depois abra INICIAR_CLIENT.bat. O MySQL e os demais requisitos da base continuam iguais. Entre no jogo para usar as funções; clicar no Menu antes disso agora apenas aguarda a interface.
