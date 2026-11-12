# Client Treino Avançado V1

Continuação direta do Cache Automático V3 presente nesta sessão. Não houve substituição por outro client nem importação de lógica de movimentação de terceiros. Backend Python/aiohttp, parser Python existente e painel ActionScript 3 dentro do carregador SWF.

## Implementação

- `TrainingSuite.as`: ciclo de vida, leitura do mapa/jogador, amostragem de posições, fantasma visual, scanner XML/nativo, trilha, marcadores, tracker, HUD, macros nativas, comandos normais de Retry, registro de tentativas e integração HTTP autenticada.
- `TrainingMenu.as`: nove abas, busca, campos editáveis, importação/exportação por FileReference, sliders, temas, arraste, atalhos, configurações e diagnóstico. O botão Treino e F8 abrem este painel; Menu continua oferecendo a interface clássica.
- `api/training.py`: SQLite por conta autenticada, validação estrita, CRUD de rotas pessoais/macros, controle otimista de versões, 20 backups por rota, comparação por índice, ranking por resultados, melhores corridas, estatísticas e logs com rotação.
- `RobotControllerReviewed.as`: snapshot público de diagnóstico e bloqueio de execução quando a sessão de treino não permite. Detecção de desvio/prisão, recuperação por comandos normais, espera pelo estado nativo e cache de rotas continuam do controlador V3.
- `RobotSuiteReviewed.as`: integração no mesmo ponto de inicialização da base. O verificador confirma preservação dos demais métodos existentes; apenas a chamada de bootstrap e os dois botões REC/SAVE são redirecionados aos componentes revisados, como no V3.
- `api/route_cache.py`: corrigida disputa entre leitura assíncrona inicial do disco e SAVE autoritativo. Um download/leitura anterior não deve substituir a rota recém-salva. Teste novo reproduz a leitura bloqueada com sincronização explícita.
- `server.py`: novo endpoint `/training_api`; autenticação existente preservada. Novo BUILD-ID obriga o iniciador a rejeitar backend antigo em execução.

## Estado e persistência

A automação nova exige consentimento explícito, identificação de sala de treino e lista nativa com um único jogador. Troca de sala limpa consentimento. Macro para com outro jogador, campo de texto, perda de foco, morte ou disputa pelos controles. Gravar macro/rota libera o Robot; não há reprodução simultânea desses recursos. Retry envia uma vez o comando configurado `mort`, `map @ID` ou `np @ID`; depende de permissão normal do servidor e desliga sem confirmação em oito segundos.

Configurações possuem debounce de 300 ms e sanitização do cache local. Uma resposta tardia de configurações não substitui alterações que o usuário acabou de fazer. Consultas têm prazo de 15 segundos e são encerradas ao remover o módulo. Listeners de estágio, overlays e controles são removidos no descarte. Erros repetidos desativam o módulo e liberam as teclas.

O ranking usa taxa de sucesso suavizada por versão da rota, quantidade de testes e atualização. Conta resultados won/dead/failed; interrupções manuais não reduzem a taxa. Falhas são agregadas por etapa, motivo e versão. Isso é aprendizado por resultados, não criação autônoma de caminhos ou treinamento de rede neural. Alterações manuais só entram na próxima tentativa; não substituem o percurso em andamento.

Rotas pessoais do novo gerenciador são locais. A publicação GitHub continua no SAVE clássico e o cache automático V3 continua disponível. Não foram sobrescritos os arquivos de rotas remotos.

SQLite: `DisneyClient/data/training.sqlite`, criado na primeira chamada autenticada. Limites: 512 rotas, 64 macros, 400 tentativas recentes e melhores corridas de até 128 mapas, 12000 amostras por tentativa, 2000 pontos de falha, 1000 logs por conta no banco. Logs em `logs-client/training-ID.jsonl`, rotação de 2 MiB e um arquivo anterior. Credenciais conhecidas são ocultadas nas mensagens. O pacote não inclui banco pessoal ou `.env` privado.

## Testes executados

| Grupo | Resultado | Ambiente |
|---|---:|---|
| Backend: rotas/cache/diagnóstico/treino | 40 testes | Python, SQLite temporário, aiohttp HTTP local |
| Nova interface e ferramentas | 55 verificações | SWF em Ruffle/Chromium, jogo e HTTP de teste |
| Ciclo de vida de treino | 11 verificações | SWF em Ruffle/Chromium, controles nativos simulados |
| Robot da base | 340 verificações | SWF em Ruffle/Chromium |
| Gravador e rascunhos | 29 verificações | SWF em Ruffle/Chromium |
| Cache/versionamento na SWF | 6 verificações | SWF em Ruffle/Chromium |
| Rota baixada com atraso | 10 verificações | SWF em Ruffle/Chromium |
| Fake Lag existente | 33 verificações | SWF em Ruffle/Chromium |
| Integridade da SWF | PASS | FFDec/Java: métodos preservados, sete classes, pilha/escopo, APIs proibidas nos módulos novos |

Os testes novos verificam: CRUD/isolamento entre contas, conflito de versão, restauração e limite de backups, comparação, ranking por versão, validação de macros/posições, melhores corridas apenas vencidas, idempotência de tentativas, logs redigidos/rotacionados, GET/POST HTTP e erros, nove abas e controles, consentimento/sala solo, XML e espelhamento, dados ausentes, checkpoints e remoção de movimento, captura de teclas e exclusão de texto, configurações assíncronas, carregamento do fantasma, HUD, ausência de mutação de posições, vitória nativa encerrando cronômetro, liberação de teclas ao entrar outro jogador, parada para digitar, Retry único e descarte.

Logs completos em `fontes-robot-revisado/resultados/treino-avancado/`. Captura da interface em `TREINO-AVANCADO-PREVIA.png`. Fixtures e fontes dos testes acompanham o projeto. `rebuild.py` recompila a partir da base e dos fontes incluídos com Java 21 + FFDec externo; o ZIP já contém a SWF compilada.

## Limites reais

Não houve teste de partida no Adobe Flash/Windows nem conexão ao servidor real de jogo. Testes de contratos, estados, HTTP e execução AVM2 não demonstram conclusão de todos os mapas em física real. Não se promete funcionamento perfeito em qualquer FPS/ping. Rotas antigas podem conter estados e não todas as teclas originais; o controlador encerra desvios excessivos, sem teleportar nem forçar queijo/vitória.

O scanner apresenta somente dados disponíveis. XML ausente, plataformas não expostas e limite de morte por queda são informados, sem coordenadas inventadas. Altura do mapa não é tratada como limite de morte. Lava: tipo conhecido 3; plataformas inclinadas aparecem como marcador central. Não há previsão completa de perigos móveis ou colisões dinâmicas.

Fantasma é uma representação vetorial visual da melhor vitória local. Uma gravação espelhada não é executada em orientação diferente. Delta usa correspondência espacial próxima e é aproximado, sobretudo em percursos que cruzam a si mesmos. Amostragem é de até 20 Hz, com interpolação visual. Ping depende do medidor nativo existente; memória é da VM Flash. Importar/exportar tem código e validação reais, mas os diálogos de arquivo do Adobe no Windows ainda precisam de validação manual.

A interface clássica e os recursos anteriores continuam no pacote. Isso não certifica todas as funções históricas em servidores externos; as restrições de treino descritas são dos módulos novos e do Robot integrado.
