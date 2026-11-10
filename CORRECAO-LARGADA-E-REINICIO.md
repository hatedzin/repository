# Correção da largada e de reinício indevido

Parte do client Frames/Rotas por Mapa entregue nesta conversa. Os arquivos de trajetos do GitHub permanecem inalterados nesta atualização.

## Evidência e alterações

No mapa mostrado pelo usuário, @122911, a primeira amostra registra x=402 e y=369, exatamente o DS de nascimento do XML enviado, mas traz um intervalo inicial de 2630ms. No conjunto fornecido, 1862 das 1964 rotas com DS comparável começam a até 5px do nascimento; 1834 dessas têm intervalo inicial positivo.

O controlador anterior iniciava esse intervalo após a preparação e o download. Agora:

- A consulta começa quando o código do mapa é identificado, inclusive durante a preparação do personagem/contagem regressiva.
- Nas rotas publicadas, o intervalo inicial é contado a partir do início observado da vida/rodada. Não é somado novamente ao tempo gasto preparando o jogo e baixando a rota. Um intervalo intencional ainda restante é preservado.
- A espera fixa adicional de 250ms não é aplicada às rotas baixadas. Continuam obrigatórios personagem/corpo/clip válidos e liberação nativa de movimento. Gravações próprias mantêm seu tempo relativo ao REC.
- Os intervalos entre os movimentos não são alterados, e nenhum JSON remoto de trajeto foi modificado.

Foi corrigido também um reinício possível no mesmo percurso: o pacote local 144/2 era tratado sempre como nascimento, mesmo se o rato continuasse vivo. Atualização de perfil/jogador não deve iniciar outra reprodução. Agora há exigência de evidência de término/morte/rodada para aceitar esse reinício.

Uma falha encerra a tentativa e solta as teclas. Atualizar o jogador ou desligar/ligar F2 não reinicia essa rota no meio da mesma vida. Nova rodada ou morte/renascimento confirmados liberam outra tentativa. O menu identifica esta versão como `Robot (largada sincronizada)` e a faixa usa `Robot largada v2`.

## O que permanece

A rota é baixada uma vez por mapa e descartada na troca; morte/renascimento no mesmo mapa reutilizam a cópia. O SAVE individual por mapa, as 2353 rotas importadas, o gravador, os logs e os demais recursos permanecem. O campo de delay herdado do menu continua sem participar do relógio do controlador; colocar zero nele não ajusta essa largada.

O avanço por ENTER_FRAME continua. Esta entrega não afirma resolver precisão em qualquer FPS: a sincronização com a física real do jogo e os pulos inferidos das rotas importadas ainda precisam ser observados em partidas reais. A mudança corrige a contagem da espera inicial e o reinício indevido, sem introduzir multiplicadores de FPS presumidos ou teleporte.

## Validação executada

- 300 verificações AS3 de reprodução em Ruffle/Chromium, incluindo a rota inicial de 2630ms, preservação da espera restante, falha que permanece encerrada após atualização de perfil e F2, e liberação após morte/renascimento confirmados.
- 29 verificações AS3 de gravação e SAVE.
- 33 verificações AS3 de integração dos hooks de Fake Lag.
- 13 testes Python do armazenamento e diagnóstico.
- Verificação estrutural: somente inicialização e REC/SAVE substituídos entre os métodos da base; cinco classes revisadas adicionadas; 125 novos corpos com pilha/escopo válidos. Demais métodos antigos permanecem idênticos.

Os resultados atualizados estão em fontes-robot-revisado/resultados. Esses testes usam objetos simulados; não foram executadas partidas reais no Windows/Flash. A imagem do usuário comprova o desvio de 287px, mas não identifica sozinha todas as causas. Esta correção não é uma declaração de que todas as rotas já foram concluídas no jogo real.

## Usar

Feche o client anterior, extraia o ZIP inteiro numa pasta nova, prepare/copie sua configuração local usando PREPARAR_PASTA.bat se necessário, e execute INICIAR_CLIENT.bat. Permanecem os requisitos da base, incluindo Python, dependências, configuração MySQL e parser funcional. Confira a identificação Robot largada v2 para ter certeza de que iniciou esta versão.
