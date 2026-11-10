# Robot revisado — relatório de entrega

Base exclusiva: `DisneyClient-Completo-Rotas-Novas-Configurador-Corrigido.zip` enviado nesta solicitação. Não foram importadas implementações de outros clientes. As classes ativas do SWF foram decompiladas para conferir a integração com os fontes desta base. As ferramentas de compilação e emulação são externas ao projeto; o código utilizado veio desta base ou foi escrito nesta revisão.

## Uso

1. Feche o client anterior e extraia o ZIP inteiro numa pasta nova.
2. Execute `PREPARAR_PASTA.bat`. Se necessário, copie sua configuração pessoal `.env` para a pasta `DisneyClient-Local-Robot-Novo/DisneyClient`.
3. Execute `INICIAR_CLIENT.bat`. Permanecem os requisitos do projeto enviado: Python, dependências, MySQL/configuração local e parser funcional. O endereço local continua `127.0.0.1`.
4. Na primeira interface pronta, o Robot é habilitado automaticamente uma vez. Ele aguarda mapa, personagem e liberação nativa, e reinicia nas próximas rodadas. Desligar no menu/F2 permanece respeitado durante a sessão. REC toma o controle e desliga a reprodução para gravar.
5. Para aproveitar a captura precisa do pulo, regrave suas rotas com esta versão. REC inicia a tentativa; concluir a toca confirma a gravação; SAVE preserva uma cópia local e tenta publicar no GitHub. A credencial continua sendo configurada somente no seu computador pelo configurador existente.

As rotas antigas do projeto continuam compatíveis e não foram apagadas. Não é possível reconstruir teclas que uma gravação anterior não registrou. Gravações de outros jogadores continuam usando estados observados, pois o client não recebe as teclas físicas deles.

## Falhas encontradas e correções

| Área | Causa no código enviado | Alteração |
|---|---|---|
| Inicialização | `auto_play` dependia de ativação externa; não havia inicialização automática do novo controlador | Ativação única através do botão nativo após a interface existir; desligamento manual respeitado nas rodadas seguintes |
| Início da rota | A espera inicial não marcava o relógio como suspenso | Primeiro avanço após uma espera começa com delta zero |
| Rodadas | Pacote de nova rodada podia ser observado antes da instalação do mapa/personagem | Liberação imediata das teclas e barreira por troca real de mapa/código/rodada/corpo, nascimento ou ciclo de bloqueio/liberação nativo; o pacote sozinho não reinicia o mapa anterior |
| Respawn | Estado terminal podia permanecer após substituição real do personagem/corpo | Reinício da vida após evidência de renascimento; vitória/morte interrompem os controles |
| Pulos gravados | Amostras periódicas de movimento e animação eram usadas para inferir a tecla; pressionar/soltar curto podia desaparecer | Captura dos eventos locais de teclado, inclusive Up/W pressionado e solto; campo opcional `up` validado no client e servidor |
| Pulos reproduzidos | Pulsos inferidos tinham duração/intervalo mínimo de 30ms | Rotas novas reproduzem o estado registrado de Up; rotas anteriores conservam a inferência compatível |
| Atrasos | Estados vencidos podiam ser alcançados rapidamente, comprimindo controles | Uma amostra de movimento por avanço; intervalos preservados sob atraso acumulado; pausas longas suspendem o relógio em vez de disparar toda a sequência atrasada |
| Desvio | Retorno de recuperação não restaurava os controles gravados | Restauração explícita e continuação do mesmo passo, usando somente teclado nativo |
| Travamento | Não havia detecção de falta de progresso durante a rota normal | Observação de deslocamento sob comando, recuperação após 1,5s sem progresso, limite de três recuperações por vida e prazo de 4s por tentativa |
| Consulta de rota | URLLoader sem prazo podia manter a fase de carregamento indefinidamente | Prazo de 25s, cancelamento ao trocar vida/mapa/desligar/remover documento e tentativa posterior; falha temporária conserva cache válido |
| Armazenamento | Havia apenas um rascunho por usuário; outra tentativa podia substituir a anterior | Arquivo local separado por usuário e mapa, validado e substituído atomicamente no SAVE |
| Reinício após SAVE falhar | Uma rota antiga do GitHub podia voltar a substituir a gravação nova pendente | A cópia local pendente tem prioridade até publicação bem-sucedida; cópia já publicada continua disponível se a consulta externa falhar |
| SAVE concorrente | Resposta de um SAVE antigo podia reinstalar uma rota após outra gravação terminar | Instalação condicionada ao conteúdo atual; confirmação de publicação local também compara os dados antes de alterar o estado |
| Gravador | Referências antigas de jogadores e tempo de contagem regressiva podiam entrar na captura | Atualização das referências; espera pela liberação nativa antes da primeira amostra; captura conserva espelhamento e seleção de jogadores |
| Tecla manual | O observador só na captura podia não receber uma tecla cujo alvo fosse o próprio Stage | Observação nas fases de captura e de alvo/propagação, com pausa idempotente e filtragem de eventos sintéticos |
| Recursos | Timer de 5ms somado a ENTER_FRAME, listeners de Stage persistentes e consultas sem limpeza | Timer de 10ms, deduplicação por timestamp, remoção/reinstalação dos listeners, fim dos carregamentos ao remover o documento e cache remoto limitado a 64 mapas |
| Observabilidade | Mensagens visuais não davam um histórico persistente do Robot | Até 100 transições na memória e eventos autenticados em `logs-client/flash-diagnostics.jsonl`, com fase, mapa e passo; limite de envio, sem dados de pacotes nem credenciais |

A recuperação é conservadora: não modifica posição, velocidade, gravidade ou colisões, não força queijo/toca e não envia pacotes de vitória/morte. Desvios grandes, falha de coleta ou recuperação esgotada interrompem a tentativa com mensagem. Não é um planejador de caminhos capaz de inventar uma rota nova num mapa incompatível.

## Arquivos modificados

Arquivos existentes alterados:

- `DisneyClient/public/ChargeurTransformice.swf`: cinco classes revisadas adicionadas; troca do ponto de inicialização do Robot e dos dois handlers REC/SAVE.
- `DisneyClient/api/github_routes.py`: validação do estado de Up, arquivo local por mapa, prioridade de pendências e proteção contra confirmação antiga.
- `DisneyClient/api/diagnostics.py`: evento autenticado `robot` e validação dos campos.
- `DisneyClient/BUILD-ID.txt`: identificação da revisão.
- `ARQUIVOS-SHA256.json`: hashes atualizados.

Arquivos novos:

- `fontes-robot-revisado/RobotControllerReviewed.as`
- `fontes-robot-revisado/RobotInputReviewed.as`
- `fontes-robot-revisado/RobotRouteReviewed.as`
- `fontes-robot-revisado/RouteRecorderReviewed.as`
- `fontes-robot-revisado/RobotSuiteReviewed.as`
- Compilador, verificador, script de reconstrução, cópia do SWF base, fontes/fixtures de teste e resultados na mesma pasta.
- Este relatório, instruções e inventário de alterações.

Os demais arquivos existentes foram comparados com a base por SHA-256. A verificação dos corpos de bytecode confirmou que os outros métodos do SWF permaneceram idênticos. Parser, Follow, Fake Lag, menu, recursos visuais, inicializador, endereço local e configuração não foram substituídos. Essa identidade estrutural não equivale a testar todas as funções numa partida real.

## Testes executados

- **264 verificações AS3 de reprodução**, executadas em Ruffle/Chromium com objetos de jogo simulados: ativação automática, desligamento manual, anexação duplicada, 30 rodadas consecutivas, mapa/vida/respawn, vitória/morte, espelhamento, controles e pulos, pausa de chat, perda de foco, corpo substituído, desvio, travamento, coleta/toca confirmadas, falta de rota e consulta HTTP realmente mantida sem resposta até o prazo de 25s.
- **29 verificações AS3 de gravação/SAVE**: eventos físicos de Up pressionado/solto, contagem regressiva, duração dos eventos, espelhamento, jogadores selecionados, morte/nova rodada, falha e repetição de SAVE e recuperação de rascunho.
- **33 verificações de integração com Fake Lag**: hooks do parser desta base aplicados à fixture; gravação e Robot compartilham callbacks, preservação de cursor, prioridade, ordem, cópia de pacotes e limpeza por ciclo de vida.
- **9 testes Python** executados contra o armazenamento e diagnóstico: validação/compressão, entradas inválidas, cópias de vários mapas, publicação simulada, preferência de pendência, isolamento por usuário, erros e escrita dos logs.
- **Verificação estrutural do SWF**: apenas inicialização e REC/SAVE alterados entre os métodos existentes, cinco classes adicionadas, 122 novos corpos com pilha/escopo válidos e nenhuma chamada do Robot a posicionamento/sincronização/pacotes forçados.
- Reconstrução executada pelo próprio `fontes-robot-revisado/rebuild.py` incluído no pacote, seguida da execução dos testes a partir da pasta de entrega.

Resultados literais estão em `fontes-robot-revisado/resultados`. Avisos de AppKey/depreciação do aiohttp aparecem nos testes e não foram tratados como aprovação de produção.

### Limites da validação

Não foram executadas partidas reais no Adobe Flash/Windows, conexão ao servidor de Transformice, teste real de MySQL/parser remoto nem publicação no GitHub com sua credencial. O cenário de publicação usa servidor/métodos simulados. Os testes de mapas e física usam fixtures: não provam que qualquer rota concluirá qualquer mapa real. Latência, objetos móveis, baixa taxa de quadros, alterações do servidor, recursos de movimento ativados ou rotas antigas sem teclas podem continuar afetando o resultado. Não houve benchmark de CPU/memória no seu computador. O parser e seus símbolos permanecem os do ZIP enviado; esta entrega não afirma corrigir incompatibilidade dele com um SWF externo atualizado.

## Reproduzir os testes

Requisitos de desenvolvimento: Java 21, FFDec, Node com Playwright, Chromium, runtime web oficial do Ruffle e dependências Python do projeto. Não são necessários para apenas abrir o client, além dos requisitos normais da base.

Na raiz do projeto:

```sh
FFDEC_JAR=/caminho/ffdec.jar python fontes-robot-revisado/rebuild.py
python -m unittest discover -s fontes-robot-revisado/tests -p 'test_*.py' -v
RUFFLE_DIR=/caminho/ruffle node fontes-robot-revisado/tests/run_tests.cjs
RUFFLE_DIR=/caminho/ruffle TEST_SWF="$PWD/fontes-robot-revisado/tests/fixtures/RecorderTests.swf" node fontes-robot-revisado/tests/run_tests.cjs
RUFFLE_DIR=/caminho/ruffle TEST_SWF="$PWD/fontes-robot-revisado/tests/fixtures/FakeLagTests.swf" node fontes-robot-revisado/tests/run_tests.cjs
```

Ajuste a sintaxe das variáveis para PowerShell/CMD se necessário. `CHROMIUM_PATH` permite indicar o executável do navegador. O script não publica rotas reais nem usa uma credencial pessoal durante os testes.
