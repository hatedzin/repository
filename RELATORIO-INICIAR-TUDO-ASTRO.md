# Inicialização conjunta e abertura do Flash

INICIAR_TUDO.bat prepara o projeto, inicia o backend, abre o site e inicia o parser. O site permanece disponível se o parser falhar. Um backend compatível aberto é reaproveitado; Ctrl+C encerra somente os processos iniciados pela janela atual. MySQL e os requisitos existentes continuam necessários.

A entrada por key volta a apresentar a URL autenticada do jogo. O usuário deve copiar essa URL para Arquivo > Abrir no Flash Player. Abrir uma SWF baixada como arquivo local perde os parâmetros de autenticação. O portal verifica a prontidão do parser antes de liberar a abertura, protege contra cliques duplicados e entrega a SWF original com o tipo de conteúdo correto. Não há alteração do robô, SWF ou fontes ActionScript.

Feche o iniciador antigo antes de aplicar. Extraia ATUALIZACAO-INICIAR-TUDO-ASTRO.zip onde está INICIAR_CLIENT.bat, mantenha as pastas e aceite substituir os arquivos da atualização. Depois execute INICIAR_TUDO.bat. A atualização inclui os arquivos do backend necessários e suporte ao pacote anterior preparado ou ainda não extraído. Configuração .env e chave privada existentes são preservadas. O ZIP V2 é a alternativa completa.

Validação: dois testes de integração com MariaDB real, 14 verificações de navegador, oito verificações ADM, recuperação de senha, quatro verificações de abertura autenticada e prontidão, três cenários do iniciador conjunto e instalação do patch em dois estados do pacote. O parser usado nos testes de abertura é controlado; não foi executado o jogo no Flash Player do Windows. Esses testes verificam o fluxo HTTP e os processos, não a execução de partidas.
