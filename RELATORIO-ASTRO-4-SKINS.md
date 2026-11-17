# CJ, Big Smoke, Minecraft e Gragas no Skin Changer

Abra INICIAR_TUDO.bat. No jogo: Menu > Ajustes > Skin Changer. As primeiras quatro opcoes sao CJ, Big Smoke, Minecraft e Gragas. Selecione a skin e ative o circulo Skin Changer. Com o recurso ligado, selecionar outra opcao troca o visual automaticamente. Desligar restaura o visual original.

As quatro imagens estao incluidas no client e sao servidas pelo backend local. Nao ha consulta a imagens externas. Os PNGs foram preservados byte por byte, inclusive a transparencia. Na exibicao, o client ignora as margens transparentes e ajusta os personagens proporcionalmente a um retangulo de no maximo 50 x 55 pixels, alinhado aos pes do rato. O Minecraft usa suavizacao desligada para preservar os pixels. As quatorze skins anteriores continuam disponiveis; use a roda do mouse sobre a lista para rolar.

Esta atualizacao parte do ZIP V3.1 enviado pelo usuario e preserva a correcao do erro #1056, Rato leve, Auto Win, Robot, Follow, portal e configuracao local. Somente um novo helper de Ajustes foi ligado na inicializacao. Os demais metodos existentes da SWF permaneceram identicos.

Para atualizar: feche o Flash e o iniciador. Extraia ATUALIZACAO-ASTRO-4-SKINS.zip onde esta INICIAR_CLIENT.bat, mantendo as subpastas e aceitando substituir os arquivos. Abra INICIAR_TUDO.bat e use a URL autenticada no Flash novamente. Nao reabra uma copia antiga da SWF salva em outra pasta. O patch nao substitui .env, banco ou chave privada. O ZIP completo V3.2 e a alternativa para instalar em outra pasta.

Validacao: 30 assercoes executadas em AS3 no emulador Ruffle, com carregamento real dos quatro PNGs pelo servidor HTTP local. Verificados os nomes, as dezoito opcoes, rolagem, limites de tamanho, alinhamento, troca com recurso ligado, respawn, restauracao e conclusao de download depois de desligar. Os hashes dos PNGs foram comparados com os arquivos originais do Skins.zip. Verificados os limites de pilha/escopo do bytecode. Ainda nao foi executado no Flash Player do Windows nem em partida real.
