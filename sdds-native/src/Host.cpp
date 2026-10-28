#include <windows.h>
#include <iostream>
#include <string>

// Test host: loads the DLL into this process only. Does not open another process.
int wmain() {
    wchar_t executable[MAX_PATH];
    if (!GetModuleFileNameW(nullptr,executable,MAX_PATH)) return 1;
    std::wstring path(executable);
    path=path.substr(0,path.find_last_of(L"\\/")+1)+L"SddsMenu.dll";
    HMODULE dll=LoadLibraryExW(path.c_str(),nullptr,LOAD_LIBRARY_SEARCH_DLL_LOAD_DIR|LOAD_LIBRARY_SEARCH_DEFAULT_DIRS);
    if (!dll) { std::wcerr<<L"Nao foi possivel carregar SddsMenu.dll. Erro: "<<GetLastError()<<L"\n";return 1; }
    using Create=HWND (WINAPI*)();using Destroy=void (WINAPI*)(HWND);
    auto create=reinterpret_cast<Create>(GetProcAddress(dll,"SddsCreateMenu"));
    auto destroy=reinterpret_cast<Destroy>(GetProcAddress(dll,"SddsDestroyMenu"));
    if (!create || !destroy) { std::cerr<<"Exports da DLL ausentes.\n";FreeLibrary(dll);return 1; }
    HWND window=create();
    if (!window) { std::cerr<<"Falha ao criar menu.\n";FreeLibrary(dll);return 1; }
    MSG message{};
    int status=0;
    while (IsWindow(window)) {
        BOOL result=GetMessageW(&message,nullptr,0,0);
        if (result<=0) { if (result==-1) status=1;break; }
        if (!IsDialogMessageW(window,&message)) { TranslateMessage(&message);DispatchMessageW(&message); }
    }
    destroy(window);
    // Registered window classes reference DLL code; keep it loaded until process exit.
    return status;
}
