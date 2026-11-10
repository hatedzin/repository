# Cache automático de rotas — V3

Base: o projeto Largada V2 entregue nesta conversa. Esta versão substitui a regra anterior de apagar rotas baixadas na troca de mapa: agora há reutilização em memória e em disco. Os arquivos de trajeto do repositório não foram modificados nesta entrega.

## Uso

Extraia o ZIP inteiro numa pasta nova, prepare a pasta/configuração pelo PREPARAR_PASTA.bat quando necessário e execute INICIAR_CLIENT.bat. A faixa deve mostrar **Robot cache v3** e a opção **Robot (cache automatico)**. Permanecem os requisitos da base: Python, dependências, MySQL/configuração e parser funcional. Não é necessário instalar Java/FFDec para abrir o client; essas ferramentas são apenas de desenvolvimento.

O Robot é habilitado uma vez quando a interface fica pronta. Desligamento manual continua respeitado. REC toma o controle para gravar; SAVE continua publicando o arquivo individual do mapa e preservando rascunhos locais quando falha.

## Fluxo implementado

Mapa identificado → rota validada na memória da SWF, quando disponível → consulta local assíncrona para validar a versão → cache do backend em memória/disco ou download do JSON daquele ID → validação → preparação para a próxima tentativa/rodada.

- O ID numérico é mapeado diretamente para `hatedzin/repository/rotas-mapas/<codigo>.json`. Não existe seleção/importação manual por mapa.
- A SWF mantém até 64 entradas recentes, incluindo dados e resultados de consulta. Uma rota em memória pode ser usada imediatamente após a liberação nativa e a prontidão do personagem.
- O backend mantém até 64 rotas em memória e até 128 arquivos/32MiB de cache gravado no disco, com descarte das entradas menos recentes. A pasta é `DisneyClient/data/rotas-cache-github`. O pacote inclui ainda uma cópia inicial de 2.353 rotas em `DisneyClient/data/rotas-iniciais`, validada contra os hashes do GitHub. Essa fonte inicial ocupa aproximadamente 16MiB, é lida por demanda e não cresce com o uso; não está incluída no limite de 32MiB do cache de rede.
- Se o disco não permitir gravação, a sessão continua usando memória. Não depende de uma autorização de SharedObject do Flash: a persistência é feita no servidor local.
- Trocar de mapa cancela apenas o interesse da SWF na resposta antiga. O download compartilhado do backend pode terminar e ficar preparado para uma volta futura ao mapa. Respostas atrasadas não substituem a rota do mapa atual.
- Durante a reprodução, a rota ativa é uma cópia fixa. Atualizações válidas substituem o cache, sem trocar os controles no meio do percurso; a versão nova é usada na próxima tentativa.

O sistema carrega JSON em memória. Não baixa, recompila ou reinicia a SWF inteira a cada mapa. A compilação ocorreu apenas para produzir esta entrega.

## Versão, integridade e rede

Para arquivos públicos, o backend usa diretamente o endereço raw do GitHub. Isso evita uma consulta de metadados antes de cada download. A resposta é limitada a 256KiB por rota e precisa passar pela validação de formato, campos, intervalos, controles e término na toca.

O backend guarda ETag e versão SHA-256. Faz verificação condicional com `If-None-Match`; quando o GitHub responde 304, não baixa o corpo novamente. Pedidos de revalidação usam controle de cache e uma janela de URL para reduzir a reutilização indevida de respostas antigas do CDN. A atualização depende da próxima verificação, da rede e da propagação do GitHub; não é uma promessa de atualização instantânea.

A consulta privada/compatível pela API valida também o SHA do blob Git quando utilizada. O catálogo anterior `rotas-novas.json` permanece como fallback de compatibilidade quando não existe um arquivo individual.

O arquivo persistente tem digest SHA-256 e é substituído atomicamente. Conteúdo corrompido não é executado. A SWF valida o ID solicitado, a versão, o esquema dos passos e um CRC32 dos dados recebidos. CRC32 é uma verificação de transporte, não uma assinatura criptográfica; a origem remota usa HTTPS, e a API local mantém a autorização da base.

A SWF pode receber uma resposta curta `unchanged` em vez de receber a mesma rota completa de novo. Verificações locais ocorrem em segundo plano a cada entrada de mapa e em intervalos de 30s durante a sessão. O backend revalida o GitHub normalmente após 60s. Se estiver preparando uma rota que ainda está sendo revalidada, a SWF pode conferir o backend novamente após 1s; isso não gera outro download remoto em paralelo.

Consultas simultâneas do mesmo ID compartilham uma tarefa. Downloads de primeiro uso têm espaço próprio de execução e não precisam esperar uma fila de pré-carregamentos. Há prazo de consulta e recuo após falhas. Mapas sem rota têm cache negativo temporário, evitando pedidos contínuos.

## Pré-carregamento

Após o primeiro acesso, o backend aquece até quatro rotas recentes encontradas no disco. Também observa transições de mapas atendidas e prepara até dois sucessores já observados. Isso é uma previsão limitada, não uma garantia de qual será o próximo mapa da sala. Não baixa as 2.353 rotas inteiras ao iniciar o client.

Para mapas presentes na cópia inicial validada, o primeiro uso pode ser atendido localmente, com verificação do GitHub em paralelo. Para mapas novos sem cópia inicial nem cache, o primeiro uso precisa da rede. Se o cache está vencido, é priorizada a última rota validada e a revalidação ocorre em paralelo. Isso atende ao fallback offline, mas significa que não se pode garantir a versão mais recente antes de cada largada sem esperar pela rede. A interface identifica a cópia em verificação. Uma remoção confirmada no GitHub invalida o cache para próximas tentativas e deixa uma marca local que impede ressuscitar uma rota removida a partir da cópia inicial. Essa marca só é apagada após receber uma rota válida novamente, quando o disco permite persistência.

## Largada e compatibilidade do Robot

A consulta começa assim que o código do mapa aparece, inclusive durante a contagem regressiva. A execução só começa com personagem/corpo/clip válidos, rota validada e movimento liberado pelo jogo. A espera fixa de 250ms foi removida também das rotas próprias: quando tudo está pronto, o primeiro comando pode sair no primeiro frame.

O client de referência `ChargeurTransformice.zip`, enviado e autorizado para consulta nesta etapa, foi lido como referência. Ele ignora o intervalo do primeiro passo e aplica posição/velocidade gravadas diretamente. Nenhuma implementação dele foi incorporada ao projeto.

A largada de rotas importadas sem teclas físicas agora ignora o intervalo inicial, de acordo com esse formato. Rotas próprias com teclas gravadas preservam o tratamento correspondente. Permanecem as proteções contra reinício por atualização de perfil, falha repetida no meio da mesma vida e comandos depois de vitória/morte. O temporizador verifica ciclo de vida; a reprodução segue os eventos de frame.

**Limite importante:** aplicar estados físicos e reproduzir teclas são métodos diferentes. A V3 mantém o controle nativo por teclas e não força posições, velocidades, queijo ou vitória. Portanto, o cache e a validação do JSON não provam que todos os percursos antigos serão reproduzidos com precisão. Não foi prometida precisão em qualquer FPS, nem foram reintroduzidos teleportes para imitar o client de referência.

## Testes executados

| Cenário pedido | Evidência executada |
|---|---|
| Mapa com rota | Download real do GitHub de @1628732; 30 passos validados; versão SHA-256 registrada |
| Mapa sem rota | Testes de resposta ausente, cache negativo e estado sem rota na SWF |
| Troca rápida de mapa | Cancelamento do solicitante sem destruir download compartilhado; dados separados por ID; validação da resposta na SWF |
| Reinício no mesmo mapa | Reutilização da cópia em memória, sem esperar pela rede |
| GitHub indisponível | Exceção remota e resposta HTTP 503 em servidor de teste, preservando última cópia validada |
| Cache | Memória, reinício usando disco, corrupção, disco indisponível e limites LRU testados |
| Rota modificada | Servidor HTTP de teste altera conteúdo/ETag; nova versão chega ao cache; SWF preserva a tentativa ativa |
| Partida antes do download | SWF realmente aguarda uma resposta HTTP atrasada de 600ms e não envia controles antes da validação |
| Execução dos passos | SWF executa os passos da fixture baixada: direções, pulo pressionado/solto, queijo/toca e vitória nativa simulada |

Resultados:

- **340 verificações AS3** gerais do controlador.
- **6 verificações AS3** de envelope versionado, atualização, cache e rejeição de conteúdo corrompido.
- **9 verificações AS3** de execução após download atrasado.
- **29 verificações AS3** do gravador/SAVE e **33** de integração com Fake Lag.
- **30 testes Python**, incluindo HTTP real local, ETag/304, cache persistente, integridade, concorrência, resposta antiga contra SAVE recente e prefetch.
- **Teste contra o GitHub real:** uma transferência de @1628732, segunda leitura pela memória e revalidação 304 sem novo corpo. Nesta execução, a consulta inicial levou aproximadamente 647.316ms e a leitura do cache em memória aproximadamente 0.048ms. São medidas isoladas do backend neste ambiente, não tempos garantidos de largada no seu computador. A primeira leitura da cópia inicial local levou 2.437ms nesta medição; o valor também está em github-real.log.
- **Auditoria de 2.353 rotas/179.410 passos:** formato validado e hashes dos blobs iguais aos publicados no GitHub. Isso verifica os dados, não a conclusão física de todos os mapas.
- **Verificação estrutural do SWF:** cinco classes revisadas, 129 novos corpos com pilha/escopo válidos; os outros métodos existentes da base permanecem idênticos, exceto os pontos de inicialização e REC/SAVE já previstos na revisão.

Os testes da SWF usaram Ruffle/Chromium e objetos de jogo simulados. Não foram executadas partidas reais no Adobe Flash/Windows, nem a conclusão das 2.353 rotas nos mapas reais. A atualização de conteúdo foi testada em HTTP local, sem alterar trajetos reais do usuário para fabricar um teste. O acesso privado pela API não foi testado com sua credencial.

Logs em `fontes-robot-revisado/resultados`; auditoria em `catalog-audit.json`. Logs de uso continuam em `logs-client/flash-diagnostics.jsonl`. Nenhum token pessoal foi incluído no pacote.

## Arquivos principais alterados

- `DisneyClient/api/route_cache.py`: novo cache com limites, persistência, compartilhamento de downloads, versões, prefetch e limpeza.
- `DisneyClient/api/github_routes.py`: protocolo v2, resposta curta, leitura pública condicional, integração com SAVE e compatibilidade anterior.
- `DisneyClient/server.py`: encerramento das tarefas do cache na saída.
- `fontes-robot-revisado/RobotControllerReviewed.as`: cache da SWF, CRC32, versões, atualização em paralelo e largada importada.
- `fontes-robot-revisado/RouteRecorderReviewed.as`: identificação da opção atualizada.
- `DisneyClient/public/ChargeurTransformice.swf`: compilação dos fontes revisados.
- Testes/fixtures, resultados, scripts de reconstrução, identificação e hashes.

O inventário completo está em `ALTERACOES-CACHE-V3.json`. Os relatórios anteriores são histórico; as regras vigentes do cache são as deste documento.

## Repetir os testes

Na raiz do projeto, com as dependências de desenvolvimento descritas nos relatórios anteriores:

```sh
FFDEC_JAR=/caminho/ffdec.jar python fontes-robot-revisado/rebuild.py
python -m unittest discover -s fontes-robot-revisado/tests -p 'test_*.py' -v
RUFFLE_DIR=/caminho/ruffle node fontes-robot-revisado/tests/run_tests.cjs
RUFFLE_DIR=/caminho/ruffle TEST_SWF="$PWD/fontes-robot-revisado/tests/fixtures/CacheTests.swf" node fontes-robot-revisado/tests/run_tests.cjs
RUFFLE_DIR=/caminho/ruffle TEST_SWF="$PWD/fontes-robot-revisado/tests/fixtures/RouteExecutionTests.swf" node fontes-robot-revisado/tests/run_tests.cjs
python fontes-robot-revisado/tests/live_github_smoke.py
```

O teste real precisa de internet. As outras fixtures usam servidor local e não publicam trajetos no GitHub. Ajuste as variáveis para CMD/PowerShell se necessário. As fixtures de RecorderTests e FakeLagTests também continuam disponíveis pelo mesmo parâmetro TEST_SWF.
