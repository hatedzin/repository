# PGIEX mainStandalone — recuperação parcial

Este pacote usa somente o mainStandalone do PGIEX recebido. O DisneyClient foi consultado como referência; seu loader, autenticação e parser não foram incorporados.

**Estado real: a SWF do loader V6 foi reconstruída e compilada. Isto ainda não é um client com todas as funções do jogo funcionando.** Faltam o contrato de símbolos compatível com o jogo e sua integração com a versão atual. Não foram testados login, entrada em sala nem funções dentro do jogo.

## Instalar no XAMPP

1. Use XAMPP com PHP 8.1 ou superior, Apache e mod_rewrite. Não é necessário MySQL para o servidor local implementado aqui.
2. Execute INSTALAR_XAMPP.bat ou copie a pasta `xampp/pgiex` para `C:\xampp\htdocs\pgiex`.
3. Ligue o Apache e abra `http://localhost/pgiex/`. Essa página mostra os arquivos ausentes. A instalação não sobrescreve uma pasta pgiex existente.
4. A SWF está em `http://localhost/pgiex/pgiex.swf`. Navegadores atuais não executam Flash. Para abri-la, use um runtime Flash standalone compatível que você já tenha; ele não acompanha este pacote.
5. Com um runtime disponível, execute `powershell -NoProfile -File .\Abrir.ps1 -Runtime 'C:\caminho\flashplayer.exe'`. Para Apache em outra porta, acrescente `-Backend 'http://localhost:8080/pgiex'`.

Sem os dados do contrato antigo, o comportamento esperado é uma mensagem de falha no backend, e a página de diagnóstico informa o que falta. Isso não indica que o jogo esteja recuperado.

## O que foi corrigido

- Novo ponto de entrada Standalone, reconstrução do preloader e compilação da SWF V6.
- Declarações de variáveis e retornos que impediam a compilação do código descompilado.
- Endereços do loader, imagens, áudio e visuais direcionados ao backend configurável, por padrão localhost/pgiex.
- Tratamento de falha HTTP, erro de segurança e timeout de 15 segundos nas requisições de texto.
- Leitura das chaves sem depender dos espaços na serialização JSON.
- Remoção do HWID e idioma romeno fixos do ramo standalone; parâmetros da SWF são respeitados.
- Captura de teclas nas configurações e atualização dos rótulos de sliders sem confundir o evento com o componente.
- Perfil visual 2 copiando o próprio perfil, callbacks de usar/copiar preservando a ação, limpeza da lista de visuais e correção do indicador salvo.
- Armazenamento local de três perfis visuais e listagem de visuais em mice.php. Os testes verificam o contrato HTTP, não sua execução dentro do jogo.
- Símbolos gráficos vazios receberam representações simples com rótulos; a arte original não está nos arquivos ActionScript exportados.

## Dependências que continuam faltando

O código original carrega primeiro `/get_pgiex_keys`, depois `/checkAS.php`, depois `/transformice`. Esses serviços não vieram no ZIP. Foram implementados leitores locais para o contrato antigo; nenhum símbolo foi inventado para fazer o diagnóstico parecer aprovado.

Os arquivos abaixo devem ser compatíveis entre si e com a mesma versão de jogo:

- `xampp/pgiex/private/metadata.json`: objeto com `GameLenght` (grafia original) e `GameDomain`, ambos strings usadas pelo código antigo para resolver propriedades.
- `xampp/pgiex/private/profile.json`: objeto original com `type`, `permissions` (array cujo primeiro elemento é objeto), `keys` (array cujo primeiro elemento é um objeto com nomes dos símbolos), e `classList` (string com nomes separados por vírgula).
- `xampp/pgiex/private/game.swf`: jogo compatível com o contrato acima. O servidor verifica a assinatura SWF, não a compatibilidade dos símbolos.

Esses arquivos NÃO estão incluídos. O parser do DisneyClient usa outro esquema e não pode ser simplesmente apontado para estas rotas. A lista de nomes referenciados pelo V6 está em `build/simbolos-referenciados.json`; ela é um inventário estático, não contém os valores necessários.

As rotas de início retornam 503 se o arquivo correspondente estiver ausente, ou 422 se seu formato for inválido. Não existe banco nem servidor de licenças PGIEX original neste pacote; esses leitores não implementam esse serviço. A função original `_6927432635` estava vazia e continua indisponível, agora com erro explícito.

`private/maps.txt` é opcional; sem ele, a API de mapas fornece um conjunto vazio real. `private/dress.json` é criado automaticamente ao salvar um visual. O servidor atende apenas a conexões locais. Não use o estado de presença de arquivos de /health como comprovação de funcionamento do jogo.

## Compilar novamente

Use Java e Apache Flex SDK 4.16.1, com playerglobal.swc 11.1:

```powershell
.\build\Compilar.ps1 -FlexHome 'C:\flex' -PlayerGlobal 'C:\playerglobal.swc'
```

O compilador gera `xampp/pgiex/pgiex.swf` a partir de `SWF/V6/ChargeurTransformice_fla/Standalone.as`. V5 foi preservado sem adaptação. Os arquivos C# originais também foram preservados, mas não fazem parte desta compilação; o host WinForms antigo não foi reconstruído.

## Verificação realizada

- Compilação do loader V6 com Apache Flex 4.16.1 e playerglobal 11.1: passou, com avisos remanescentes do código exportado.
- Sintaxe dos quatro scripts PHP: passou em PHP 8.4.24.
- Doze verificações de integração HTTP: passaram. Abrangem erros de dependências, validação de payloads, entrega da SWF, mapas vazios, bloqueio do diretório privado e persistência de visuais.
- Windows, Apache/XAMPP, PowerShell, runtime Flash e jogo ao vivo: não executados neste ambiente Linux. A reescrita do Apache deve ser conferida na instalação; os testes HTTP usaram o servidor embutido do PHP.

O relatório dos testes está em `build/validacao.json` e o log real do compilador em `build/compilacao.log`.
