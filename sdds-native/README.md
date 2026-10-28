# Sdds cheats — projeto C++ nativo

Esta solução produz uma DLL de interface (`SddsMenu.dll`) e um host de teste
(`SddsHost.exe`) que carrega essa DLL no próprio processo. A interface usa Win32/GDI
e controles nativos, sem navegador, Python ou dependências externas.

## Compilar no Windows

1. Instale Visual Studio 2022 com **Desenvolvimento para desktop com C++**,
   toolset v143 e Windows SDK.
2. Abra `SddsNative.sln` e selecione **Release | x64**.
3. Compile a solução. Execute `bin\x64\Release\SddsHost.exe`.

Ou, no Developer Command Prompt do Visual Studio:

```bat
msbuild SddsNative.sln /m /p:Configuration=Release /p:Platform=x64
bin\x64\Release\SddsHost.exe
```

O menu possui abas, interruptores e sliders com estado local. Todas as opções
são demonstrações visuais. Esta base não implementa chams, aimbot, alterações de
memória, hooks de renderização, injetor, bypass de anticheat ou integração com
Combat Arms. Também não integra o login Python à DLL: o sistema de keys permanece
no projeto `sdds-cheats`. Carregar esta DLL com um injetor não implementa essas funções.

`include/Menu.h` documenta os exports. Um aplicativo controlado pelo desenvolvedor
pode chamar `SddsCreateMenu` na thread de interface e manter seu message loop.
Chame `SddsDestroyMenu` antes do encerramento. Não chame os exports de DllMain.
O host mantém a DLL carregada até sair para preservar as classes de janela.

## Material recebido e validação

## EXE de console com key

`dist/SddsKey.exe` é um executável Windows x64 compilado com MinGW-w64.
Ele pede somente a key, aguarda Enter e consulta `http://127.0.0.1:8085/api/license`.
Somente após resposta positiva mostra `inicie combat arms brazil valofe`.
Key inválida, vencida ou revogada não libera essa mensagem. O prazo começa no
primeiro uso, conforme o servidor. O EXE não tem senha ou key mestra embutida.

No pacote `SddsKey-Windows.zip`:

1. Extraia tudo. Abra `sdds-cheats/configurar-admin.cmd` para criar o admin,
   caso ainda não exista. O servidor requer Python 3.11+.
2. Abra `sdds-cheats/start.bat` e mantenha aberto.
3. Use `sdds-cheats/admin.cmd` para gerar uma key de 30 ou 60 dias.
4. Execute `SddsKey.exe`, digite a key e pressione Enter.

Se já possui contas/keys, preserve seu `sdds.sqlite3` e use seu servidor existente.
O EXE não precisa de Python, mas o servidor incluído precisa. O serviço é local;
para distribuir o cliente a outras máquinas, um servidor remoto HTTPS ainda precisa
ser implementado e configurado. Este EXE não carrega a DLL nem injeta no jogo.

A compilação do EXE foi concluída no Linux via MinGW; sua execução no Windows
permanece não verificada. A DLL e o host Visual Studio continuam sem compilação.

## Referências das offsets

O arquivo enviado contém oito TXT com trechos e offsets, sem um SDK ou projeto
completo. Os originais estão preservados em `reference/`, como documentação;
não são compilados nem tratados como offsets válidos para uma build específica.
“VALOFE 2026” não identifica uma build de executável.

Este ambiente é Linux e não possui MSVC nem Windows SDK. A estrutura dos projetos
foi verificada, mas compilação e execução no Windows permanecem não verificadas.
Não há DLL compilada incluída no pacote. O EXE de console descrito acima está incluído.
