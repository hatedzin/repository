# ASTRO independente — morrer quando alguém entrar na toca

Abra ASTRO-INDEPENDENTE-MORTE-NA-TOCA.swf diretamente no Flash Player.
Em Jogador, marque “Morrer quando alguém entrar na toca”.
A opção usa a confirmação de vitória de outro jogador recebida do servidor
para executar o comando nativo `mort` do jogo incorporado.

Não dispara pela própria vitória, com a opção desligada, sem personagem,
com personagem morto, em pacotes incompletos ou novamente pelo mesmo evento.
Rearma após renascimento e limpa os eventos na troca de rodada/mapa.
A mudança não depende do Farm Time nem do Auto mort temporizado.

Mantém o menu, as skins e os 36 recursos incorporados da SWF independente.
Não precisa de CMD, parser ou backend local.

Validação: 19 verificações de eventos em execução AS3 no Ruffle;
verificação dos limites de pilha/escopo de 2080 métodos;
36 recursos incorporados idênticos aos originais;
13 verificações de inicialização, vínculo nativo, navegação e skins na interface real incorporada.
A validação de uma sala online no Flash Player do Windows permanece pendente.
