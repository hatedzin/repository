# Atualização — frames e rota temporária por mapa

Esta atualização parte do client revisado entregue anteriormente e incorpora os três arquivos de dados enviados nesta conversa.

## Comportamento solicitado

1. Ao entrar num mapa/rodada, o client solicita a rota daquele código ao backend local.
2. O backend consulta `hatedzin/repository/rotas-mapas/<codigo>.json` no GitHub. Para compatibilidade, se esse arquivo não existir, ainda consulta o catálogo anterior `rotas-novas.json`.
3. A cópia recebida fica na memória do SWF. Não é consultada novamente a cada 10 segundos nem durante a reprodução. Morte e renascimento no mesmo mapa reutilizam a cópia.
4. Na troca de mapa/rodada, a cópia baixada é descartada e a nova rota é solicitada. Voltar ao mesmo código após uma troca provoca novo download.
5. Se a consulta falhar, o client informa o motivo; desligar e ligar F2 permite tentar novamente. Não há consulta repetitiva durante o mesmo mapa.

O descarte se refere às cópias baixadas. As gravações feitas por você, os rascunhos e as cópias locais de SAVE permanecem preservados. Uma tentativa local pendente continua disponível se o GitHub estiver indisponível. SAVE agora publica o JSON apenas do mapa gravado, usando SHA e repetição limitada em caso de conflito. Não precisa reescrever todo o catálogo para salvar uma rota.

## Correção de frames

Foi reproduzida uma falha da versão anterior: as chamadas do temporizador avançavam o pressionar/soltar do pulo sem que um novo evento ENTER_FRAME tivesse ocorrido. Essa reprodução gerou a falha esperada no teste de regressão, registrada nos resultados.

O temporizador agora verifica o estado do jogo, desligamento e mudanças de vida. Somente ENTER_FRAME avança a reprodução e libera pulsos normais. O relógio de reprodução usa o intervalo entre frames, separado do relógio do temporizador; chamadas no mesmo timestamp não roubam o delta do frame. Isso evita consumir vários estados de entrada entre frames. Não altera a física nem injeta posições/velocidades.

O log `logs-client/flash-diagnostics.jsonl` agora inclui campos opcionais `fps_x10`, `target_fps_x10`, `frame_ms`, `late_ms` e `error_px`. `fps_x10=250` significa 25 FPS. A medição usa eventos ENTER_FRAME; não é uma medição interna de passos do Box2D. O FPS precisa de uma janela de amostragem para estabilizar. Não foi inventado um valor de ping: a origem da falha no seu computador ainda precisa ser confirmada pelos dados reais.

## Importação dos JSONs enviados

- `maps.json`: 2.359 entradas lidas; 2.353 rotas válidas, totalizando 179.410 passos após normalização.
- `record_list.json`: informações de recordes, nomes e tempos; não contém os movimentos do percurso.
- `protectedmaps.json`: XML de 2.354 mapas; não contém trajetos de teclas.
- Seis entradas não foram publicadas como rotas: duas com códigos não numéricos e quatro incompletas/inválidas. A lista está em `dados-rotas-enviados/IMPORTACAO-RESULTADO.json`.
- Em 102 rotas foram removidos eventos cosméticos `emote` que armazenavam textos de pacotes. O tempo deles foi incorporado ao próximo passo. Foram comparados todos os controles restantes e a soma exata dos intervalos de cada uma das 2.353 rotas.

Os arquivos originais estão guardados em `dados-rotas-enviados`, fora dos endpoints públicos e sem carregamento integral automático. Não foram importadas implementações de outros clients. Rotas desse formato descrevem estados observados, e não as teclas físicas de quem as gravou; elas continuam usando a inferência compatível de pulo. A atualização não consegue reconstruir eventos que não estão nesses arquivos.

## Testes executados nesta atualização

- **291 verificações AS3 de reprodução** em Ruffle/Chromium: incluem watchdog entre frames, pulso inferido e exato, timestamp compartilhado, intervalos simulados de 10/20/30/60/120 FPS, descarte da rota na troca, reutilização no mesmo mapa e cenários da revisão anterior.
- **29 verificações AS3 de gravação**.
- **33 verificações AS3 de integração com Fake Lag**, usando os hooks do parser desta base em fixtures.
- **13 testes Python**: incluem obtenção de arquivo individual, ausência de leitura do catálogo inteiro quando a rota individual existe, criação por mapa, repetição de conflito com novo SHA, validação dos campos de tempo e persistência local.
- **2.353 rotas importadas** validadas; controles e duração total comparados com os dados de origem.
- **Verificação estrutural**: demais métodos existentes do SWF permanecem idênticos; cinco classes revisadas adicionadas; 125 corpos novos com pilha/escopo válidos.

A regressão da versão anterior falhou de propósito ao demonstrar o problema; os testes da versão corrigida passaram. Os arquivos em `fontes-robot-revisado/resultados` registram ambos os resultados com nomes distintos.

Ainda não foram testadas partidas reais no seu Windows/Flash, todas as rotas nos mapas reais ou desempenho no seu computador. Baixar a rota uma vez remove consultas durante a execução, mas não remove ping do jogo, variação de física ou quedas de FPS. Uma rota pode continuar incompatível com um mapa/estado diferente. O parser permanece o da base enviada.

## Arquivos alterados nesta atualização

- `fontes-robot-revisado/RobotControllerReviewed.as` e seu SWF compilado: avanço por frame, diagnóstico de tempo e cache limitado ao mapa atual.
- `DisneyClient/api/github_routes.py`: leitura e SAVE por arquivo de mapa.
- `DisneyClient/api/diagnostics.py`: validação dos campos de tempo.
- Fontes/fixtures de teste, resultados, identificação do build e manifesto SHA-256.
- Dados de origem, resultado de importação e estas instruções.

O relatório da revisão anterior continua em `RELATORIO-ROBOT.md` como histórico. Os totais e o comportamento desta atualização são os descritos aqui.

## Abrir

Extraia tudo numa pasta nova, use PREPARAR_PASTA.bat se precisar copiar sua configuração e depois INICIAR_CLIENT.bat. Permanecem os requisitos normais da base: Python, dependências, MySQL/configuração e parser funcional. Os testes de desenvolvimento podem ser repetidos pelos mesmos comandos do relatório anterior.
