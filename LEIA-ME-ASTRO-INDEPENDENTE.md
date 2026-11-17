# ASTRO independente - arquivo unico SWF

Abra ASTRO-INDEPENDENTE-SEM-CMD.swf pelo Adobe Flash Player: Arquivo > Abrir > selecione o arquivo. O jogo processado e as modificacoes do V4 estao dentro da SWF. Nao e necessario iniciar CMD, Python, parser, MySQL ou o site do client. A partida continua usando a internet e os servidores do Transformice.

Incluidos: menu moderno, previas das skins, rolagem arrastavel, CJ, Big Smoke, Minecraft, Gragas e os visuais anteriores; controles de FPS, Rato leve, Robot, gravacao e Follow existentes. A taxa configurada de FPS e um pedido ao Player; o contador continua medindo os frames observados.

Rotas e preferencias: SAVE grava no armazenamento local do Flash, neste computador. O pedido so recebe sucesso depois que o Flash confirma a gravacao. Na aba Robot, os botoes Exportar rotas JSON e Importar rotas JSON permitem transferir as rotas. As rotas antigas salvas no backend nao sao transferidas automaticamente. Se o armazenamento do Flash for negado ou apagado, use seus arquivos JSON para recuperar as rotas.

GitHub: a publicacao automatica do SAVE que dependia do token guardado no backend foi substituida pela gravacao local. Nenhum PAT, senha do banco ou credencial de conta foi embutido. O portal GM/ADM e o servico de musica via backend continuam no projeto completo; nao sao executados por este arquivo.

Base do jogo: a SWF incorpora a base processada e os 138 simbolos enviados pelo usuario. Eles correspondem a essa versao do jogo. Uma atualizacao do servidor pode exigir gerar outra SWF com uma base nova. O arquivo habilita o modo de rede para SWFs locais. Se o Flash apresentar um bloqueio de seguranca local, use as configuracoes globais de seguranca do proprio Player para autorizar este arquivo.

Validacao realizada: o jogo embutido carregou e a interface real abriu no Ruffle sem chamadas ao backend ou parser. Foram verificadas as seis abas, as quatro previas de skins sem HTTP para imagens e os controles de importar/exportar rotas (12 verificacoes). Outros 22 testes AS3 verificaram os recursos embutidos, simbolos, SAVE local, rascunho, exclusao, configuracao e cancelamento de carregamento. A persistencia foi confirmada recarregando a SWF; as consultas locais nao fizeram requisicoes HTTP. Os 36 recursos embutidos foram comparados byte por byte com os arquivos de entrada. Os limites de pilha e escopo dos 2068 metodos foram verificados.

Limite do teste: nao foi validado login ou entrada em sala no Adobe Flash Player do Windows. O Ruffle deste ambiente nao tinha proxy para a conexao TCP do jogo e os recursos remotos do jogo encontraram restricoes de CORS; a interface e o jogo embutido foram carregados, mas isso nao comprova uma partida online. O arquivo deve ser conferido no Flash Player do usuario.

SHA256 do arquivo: 51c82e09a1f5a10c23e87305a444e529c294cebc4f9a0b8d01192735cbb1d1d4
