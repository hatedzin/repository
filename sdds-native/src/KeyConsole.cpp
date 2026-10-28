#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <winhttp.h>
#include <iostream>
#include <string>
#include <algorithm>
#include <cctype>

struct Internet {
    HINTERNET handle;
    explicit Internet(HINTERNET value) : handle(value) {}
    ~Internet() { if (handle) WinHttpCloseHandle(handle); }
    Internet(const Internet&) = delete;
    Internet& operator=(const Internet&) = delete;
    operator HINTERNET() const { return handle; }
};

enum class Result { Active, Rejected, Offline };

Result Validate(const std::string& key) {
    Internet session(WinHttpOpen(L"SddsKeyConsole/1.0", WINHTTP_ACCESS_TYPE_NO_PROXY,
        WINHTTP_NO_PROXY_NAME, WINHTTP_NO_PROXY_BYPASS, 0));
    if (!session.handle) return Result::Offline;
    WinHttpSetTimeouts(session, 5000, 5000, 5000, 10000);
    Internet connection(WinHttpConnect(session, L"127.0.0.1", 8085, 0));
    if (!connection.handle) return Result::Offline;
    Internet request(WinHttpOpenRequest(connection, L"POST", L"/api/license", nullptr,
        WINHTTP_NO_REFERER, WINHTTP_DEFAULT_ACCEPT_TYPES, 0));
    if (!request.handle) return Result::Offline;
    std::string body = "{\"key\":\"" + key + "\"}";
    if (!WinHttpSendRequest(request, L"Content-Type: application/json\r\n", static_cast<DWORD>(-1),
        &body[0], static_cast<DWORD>(body.size()), static_cast<DWORD>(body.size()), 0)
        || !WinHttpReceiveResponse(request, nullptr)) return Result::Offline;
    DWORD status = 0, size = sizeof(status);
    if (!WinHttpQueryHeaders(request, WINHTTP_QUERY_STATUS_CODE | WINHTTP_QUERY_FLAG_NUMBER,
        WINHTTP_HEADER_NAME_BY_INDEX, &status, &size, WINHTTP_NO_HEADER_INDEX)) return Result::Offline;
    if (status != 200) return Result::Rejected;
    std::string response;
    char buffer[1024];
    DWORD read = 0;
    do {
        if (!WinHttpReadData(request, buffer, sizeof(buffer), &read)) return Result::Offline;
        response.append(buffer, read);
        if (response.size() > 16384) return Result::Rejected;
    } while (read);
    response.erase(std::remove_if(response.begin(),response.end(), [](unsigned char c) {return std::isspace(c) != 0;}),response.end());
    return response.find("\"active\":true") != std::string::npos ? Result::Active : Result::Rejected;
}

void Pause() {
    std::cout << "\nPressione Enter para sair..." << std::flush;
    std::string line;
    std::getline(std::cin,line);
}

int main() {
    SetConsoleTitleW(L"Sdds cheats - Key");
    std::cout << "=== SDDS CHEATS ===\n\nDigite sua key e pressione Enter: " << std::flush;
    std::string key;
    if (!std::getline(std::cin,key)) return 1;
    const bool valid = !key.empty() && key.size() <= 128
        && std::all_of(key.begin(),key.end(),[](unsigned char c) {return std::isalnum(c) || c == '-' || c == '_';});
    if (!valid) {std::cout << "\nKey invalida.\n";Pause();return 1;}
    std::cout << "\nValidando key...\n";
    Result result = Validate(key);
    SecureZeroMemory(&key[0],key.size());
    if (result == Result::Offline) {
        std::cout << "Servidor de licencas indisponivel. Inicie start.bat do pacote sdds-cheats.\n";
        Pause();return 1;
    }
    if (result != Result::Active) {
        std::cout << "Key invalida, vencida, revogada ou limite de tentativas atingido.\n";
        Pause();return 1;
    }
    std::cout << "\nKey validada.\n\ninicie combat arms brazil valofe\n";
    Pause();return 0;
}
