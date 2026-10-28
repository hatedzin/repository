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

O arquivo enviado contém oito TXT com trechos e offsets, sem um SDK ou projeto
completo. Os originais estão preservados em `reference/`, como documentação;
não são compilados nem tratados como offsets válidos para uma build específica.
“VALOFE 2026” não identifica uma build de executável.

Este ambiente é Linux e não possui MSVC nem Windows SDK. A estrutura dos projetos
foi verificada, mas compilação e execução no Windows permanecem não verificadas.
Não há DLL compilada incluída no pacote.
