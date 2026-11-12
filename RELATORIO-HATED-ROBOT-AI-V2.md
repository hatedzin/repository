# HATED ROBOT AI V2 — Autonomous Navigation Engine

Implementação nova sobre o ZIP `DisneyClient-Completo-Rotas-Novas-Configurador-Corrigido.zip` enviado nesta solicitação. O conteúdo foi extraído do `client-completo.tar.xz` do próprio ZIP. Não foram reaplicados Cache V3, Treino Avançado ou funções descartadas.

## Arquitetura

- **HatedGeometry:** lê o XML exposto na SWF, terrenos/queijo/toca, espelhamento e apoios; transforma retângulos inclinados e testa um envelope aproximado do personagem. Referências nativas complementam queijo/toca quando disponíveis. Geometria desconhecida é diagnosticada.
- **HatedPhysics:** observa velocidade nativa em unidades convertidas para pixels, impulso de salto, gravidade mediana e frenagem; valida/versiona perfis. Calcula tempo de voo e previsão de pouso. Não escreve velocidade, gravidade ou posição no jogo.
- **HatedPlanner:** busca A* com preferência por trajetórias anteriores, grafo de apoios e candidatos de caminhada/salto. Validação incremental de colisão, incluindo pontos intermediários do arco. Rotas salvas são guias de custo, sem execução cega de coordenadas ou tempos antigos.
- **HatedController:** máquina de estados, prontidão nativa, execução de teclas por NativeMotion, alinhamento de decolagem, controle horizontal no ar, confirmação de objetivos, observação/calibração, recuperação limitada, interrupção manual, cancelamento de carregamento antigo e limpeza de recursos.
- **HatedLearning:** resultados associados ao mapa, assinatura de geometria e versão de física; histórico de falhas, saltos observados, correções, trajetórias vencedoras e seleção por confiabilidade. Persistência local por SharedObject e fallback em memória quando não permitida.
- **HatedMenu:** área no menu existente e painel próprio HATED ROBOT AI, ativação, opções, limite de recuperação, diagnóstico, exportação e publicação opcional. Atalho F8.
- **HatedSuite:** ponto de inicialização novo; mantém RouteRecorderV4.
- **api/hated_ai.py:** arquiva snapshots autenticados e publica arquivos novos em namespace separado no GitHub, com validação, SHA-256, limites locais e logs rotacionados. Não sobrescreve `rotas-novas.json` nem arquivos remotos existentes.

As interfaces reaproveitadas são as do próprio ZIP: NativeMotion para transições normais, RobotRoute para interpretar o formato legado, eventos nativos, SharedObject, endpoint GitHub e menu. A lógica de decisão/execução do RobotControllerV6 não foi copiada para o motor novo. O backend mantém autenticação, sockets e demais endpoints.

## Estados e execução

`IDLE`, `WAITING`, `ANALYZING`, `PLANNING`, `MOVING`, `RECOVERING`, `CHEESE`, `HOLE`, `FINISHED`, `ERROR`.

Uma rota compatível pode orientar o custo da busca; sem rota, o planejador usa geometria e física observada. Nenhuma conexão GitHub é necessária para planejar um mapa estático compatível. A opção de não jogar sem rota aguarda uma consulta limitada antes de informar ausência.

A calibração automática é conservadora: exige apoio plano largo, margem lateral e espaço superior conhecido; usa corrida curta e salto ordinário. A física continua pertencendo ao jogo. A falta de amostras ou local adequado gera mensagem, sem inventar parâmetros. O perfil continua sendo observado durante a tentativa.

O modelo mede também a relação entre deslocamento real e velocidade nativa (`timeScale`), ajustando impulso, velocidade e gravidade quando o relógio da física avança em outro ritmo. Há casos simulados com escala de física 0,5 e 1,75, além das taxas de renderização. Isso não equivale a garantir qualquer combinação real de FPS/latência.

O controlador usa tempo decorrido, libera entradas após frame longo e não dispara uma fila de saltos atrasados. O planejamento verifica no máximo 24 operações/amostras por chamada, com orçamento alvo de 3 ms; há limites de 384 apoios, 256 terrenos, 512 expansões, 50000 operações e 8 segundos por planejamento. São limites de trabalho, não promessa de tempo rígido de CPU.

Uma queda não é contada como progresso só por alterar a posição: o desvio vertical é verificado antes do progresso. Recuperação solta teclas, bloqueia o trecho problemático e tenta outra ligação. A ausência de apoio após recuperação encerra a tentativa depois de 2,5 segundos. Chegar perto do objetivo exige aproximação final e confirmação nativa. Coletar queijo no ar preserva o pouso planejado antes de mudar de objetivo.

Vitória de outro jogador é ignorada. A vitória local exige evento nativo; perfil de jogador vivo não reinicia uma vida já concluída. Nova rodada, novo corpo/renascimento e morte possuem tratamento separado. Mudança de mapa invalida consultas antigas e o planejador anterior. O motor não altera estado de outros jogadores.

## Persistência e integração

SharedObject `hatedRobotV2`: 32 mapas/geometrias, três trajetórias por mapa, física versionada e falhas recentes. Trajetórias têm até 6000 amostras, coletadas com intervalo mínimo de 80 ms e deslocamento mínimo. Guias remotos/legados têm limite de 512 pontos úteis. Cache de geometria: oito entradas; log em memória: 150 decisões.

O resultado de uma tentativa altera a confiabilidade da trajetória realmente selecionada. Falhas guardam posição/motivo; novas vitórias podem criar outra trajetória. Isso é aprendizado de parâmetros observados e resultados, não treinamento de rede neural nem descoberta universal de estratégias.

Snapshots vencedores são arquivados no backend em `data/hated-ai-v2/<conta>/`, até 64 arquivos. GitHub é opcional e começa desligado. Usa o token do configurador existente no backend, sem embuti-lo na SWF. GET verifica o destino e PUT cria sem `sha`; arquivo existente diferente causa conflito e é preservado. Arquivo idêntico é idempotente. Os snapshots AI V2 são um formato próprio; a consulta do catálogo legado continua fornecendo guias. Este trabalho não cria um sincronizador global de todos os snapshots AI V2 de outras instalações.

Logs de arquivo registram mapa/assinatura/evento sem token. Publicação possui prazo e mantém dados locais em falhas. Exportação usa diálogo real FileReference; permissões do Flash continuam aplicáveis.

## Verificação automatizada

Os resultados finais e comandos reproduzíveis acompanham `fontes-hated-ai/resultados/` e `VALIDACAO-HATED-AI-V2.json`.

- Navegação/física/controlador: mapas planos sem rota em 15/30/60/120 FPS simulados, vãos em taxas diferentes, calibração observada, queijo no ar, parede alta, lava, formas não mapeadas, recuperação limitada, queda inesperada, agachamento guiado, comandos liberados e raiz AS3 selada.
- Menu/aprendizado: botões reais, todas as opções ON/OFF, limite de tentativas, persistência, ranking, atribuição de falhas e limite de memória.
- Assíncrono/ciclo de vida: HTTP atrasado, troca rápida de mapa, descarte de resposta antiga, presença de outros jogadores, vitória/queijo de terceiros, frame longo, rodada, perfil vivo e renascimento.
- Backend novo: validação, arquivos locais reais, isolamento de conta, quota, HTTP local, autorização, publicação GitHub com transporte simulado, idempotência e preservação de arquivo remoto existente.
- Regressão: gravador/rascunhos e Follow em SWF, configurador, identidade do backend, catálogo GitHub e catálogo legado vazio em Python.
- Verificador estrutural: sete classes novas; apenas a referência do bootstrap foi alterada nos métodos originais. Os demais métodos existentes mantêm seus bytes. Pilha/escopo AVM2 válidos. Nenhum módulo novo chama APIs de posicionamento, sincronização forçada, queijo, toca ou morte.

O pacote contém fontes, SWF de produção, fixtures, prévia da interface e scripts de reconstrução com Java 21/FFDec externo. O `BUILD-ID` atualizado permite ao iniciador detectar um backend antigo ainda aberto.

## Resultados desta build

| Grupo | Resultado |
|---|---:|
| NavigationTests | 95 verificações SWF |
| InterfaceTests | 61 verificações SWF |
| AsyncTests | 16 verificações SWF |
| RecorderRegression | 26 verificações SWF |
| FollowRegression | 27 verificações SWF |
| backend | 8 testes Python |
| python-configurator | 6 testes Python |
| python-identity | 1 testes Python |
| python-legacy_github | 14 testes Python |
| python-legacy_catalog | 1 testes Python |

## Limites e validação real pendente

**Não houve partida em Adobe Flash/Windows nem conexão a um servidor real de jogo.** Os testes executam SWF real em Ruffle/Chromium com física e eventos sintéticos; os testes HTTP usam servidor local e transporte GitHub substituído. Não comprovam conclusão de todos os mapas ou ausência de DC no servidor real. Não foi feita publicação de rotas de teste no catálogo do usuário.

A base não fornece uma representação completa de contatos/fixtures físicas, forma exata do corpo, permissão de salto no ar ou toda a física de superfícies especiais. O envelope usado é aproximado; apoio deriva da geometria e estabilidade da velocidade, não de um contato nativo completo. Caminhos e colisões inclinadas são previstos por um modelo conservador, ainda sem certificação em partidas reais.

Círculos, corpos dinâmicos, objetos físicos do XML sem geometria mapeada e inclinações extremas param com diagnóstico. Superfícies especiais não modeladas não são apoios válidos. Objetos criados durante a rodada podem não estar no XML; gelo, vento, gravidade não convencional e mecanismos complexos exigem outro modelo. Não há salto duplo forçado; saltos seguintes requerem novo apoio. Agachar não é tratado como redução de corpo, pois isso não foi comprovado nessa base.

Rotas antigas podem não conter todas as teclas originais. Por isso são guias geométricos, não promessa de reprodução idêntica. O planejador pode rejeitar um mapa solucionável quando o modelo ou os limites atuais não bastam; o diagnóstico preserva essa distinção. Desempenho e latência reais podem alterar o resultado. A ferramenta não promete resolver qualquer mapa em qualquer FPS/ping.
