# ASTRO MENU RGB V3 — painel disponível no login

A V2 apenas aguardava a interface nativa e podia continuar mostrando “Entre no jogo” mesmo dentro da sala. A V3 abre o painel independentemente dessa interface e conecta os controles reais depois, no mesmo painel. O campo Interface tipado do client não recebe um objeto simulado.

## Mudanças

- Painel, navegação, opacidade, fechar/reabrir e título RGB disponíveis antes de entrar numa sala.
- Inicialização dos controles nativos retomada quando suas classes estão resolvidas; eliminada a espera circular da V2.
- Removida somente a chamada da moldura antiga SafeMarket/set_box, substituída pelo desenho ASTRO, do construtor original de apresentação.
- Ligação dos controles reais preserva os listeners, as funções, a aba selecionada e o painel aberto/fechado.
- Falhas na montagem nativa não bloqueiam o painel: código exibido dentro da aba, até três tentativas por ciclo, com retomada por clique ou mudança de jogador/Keys.
- Sem alteração do robô, Follow, gravador, rotas, entrada nativa, Statements, backend, parser ou autenticação.

## Validação

22 verificações de abertura imediata, interface parcial, falha de construtor, ligação de controles, preservação de callback e fechar/reabrir passaram em Ruffle. Passou um cenário adicional com a classe MainTimeline tipada real, confirmando que o painel aparece sem sobrescrever Interface. Os 32 testes de visual/RGB também passaram.

Comparação estrutural: 1.596 corpos de métodos antigos idênticos. Além dos ajustes visuais já existentes, o construtor de UI perde apenas as 16 instruções da moldura antiga. Métodos protegidos do robô, Follow, REC, entrada nativa e Statements estão idênticos ao ZIP base. 91 corpos de apresentação verificados.

Esses testes são fixtures: a MainTimeline real é usada com a inicialização de rede substituída. A ligação de controles é simulada. Não houve sessão real do jogo no Windows/Adobe Flash, nem verificação de gameplay ou rotas. A captura incluída representa um fixture de abertura do painel, não login conectado.

## Uso

Feche o Flash e o client antigo. Extraia este ZIP em outra pasta, abra PREPARAR_PASTA.bat e copie sua .env anterior para DisneyClient-Local-Robot-Novo/DisneyClient/.env, se necessário. Abra INICIAR_CLIENT.bat. O painel já pode abrir no login; os controles dependentes do jogo se conectam quando a interface nativa fica disponível. MySQL e requisitos da base continuam os mesmos.
