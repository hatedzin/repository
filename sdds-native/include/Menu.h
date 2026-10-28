#pragma once
#include <windows.h>

#ifdef SDDS_EXPORTS
#define SDDS_API extern "C" __declspec(dllexport)
#else
#define SDDS_API extern "C" __declspec(dllimport)
#endif

// Call on the UI thread, outside DllMain. The caller owns the message loop.
SDDS_API HWND WINAPI SddsCreateMenu();
SDDS_API void WINAPI SddsDestroyMenu(HWND window);
