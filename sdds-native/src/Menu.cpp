#include "Menu.h"
#include <array>
#include <string>
#include <cwchar>
#include <commctrl.h>

namespace {
constexpr wchar_t ClassName[] = L"SddsNativeMenu";
constexpr COLORREF Background = RGB(28,28,34);
constexpr COLORREF Accent = RGB(19,136,249);
const std::array<const wchar_t*, 11> Tabs = {
    L"VISUAL",L"ESP",L"COLORS",L"AIMBOT",L"REMOTE",L"WEAPON",
    L"PLAYER",L"VIPS",L"UTIL",L"CONTA",L"ADMIN"
};
const std::array<const wchar_t*, 19> Options = {
    L"NX Chams",L"No Fog",L"No Smoke",L"No Flash",L"Full Brightness",
    L"Player Brightness",L"No Weapon",L"Remove Texture",L"Zombie Effect",
    L"Frozen Effect",L"Remove Crosshair",L"No Sky",L"White Walls",
    L"Night Mode",L"RenderBlocks",L"WorldTree",L"Show FPS",L"Darkness Effect",L"TAG Names"
};
struct State {
    int tab = 0;
    std::array<bool, 19> enabled{};
    HFONT font = nullptr;
    HBRUSH background = nullptr;
    HWND sharpness = nullptr;
    HWND sky = nullptr;
};

void Fill(HDC dc, RECT r, COLORREF color) {
    HBRUSH brush = CreateSolidBrush(color);
    FillRect(dc, &r, brush);
    DeleteObject(brush);
}
void Text(HDC dc, const wchar_t* text, RECT r, COLORREF color, UINT align = DT_LEFT) {
    SetTextColor(dc, color);
    DrawTextW(dc, text, -1, &r, align | DT_SINGLELINE | DT_VCENTER);
}

LRESULT CALLBACK Procedure(HWND window, UINT message, WPARAM wp, LPARAM lp) {
    auto* state = reinterpret_cast<State*>(GetWindowLongPtrW(window, GWLP_USERDATA));
    switch (message) {
    case WM_CREATE: {
        state = new State;
        SetWindowLongPtrW(window, GWLP_USERDATA, reinterpret_cast<LONG_PTR>(state));
        state->font = CreateFontW(-13,0,0,0,FW_NORMAL,FALSE,FALSE,FALSE,DEFAULT_CHARSET,
            OUT_DEFAULT_PRECIS,CLIP_DEFAULT_PRECIS,CLEARTYPE_QUALITY,DEFAULT_PITCH,L"Segoe UI");
        state->background = CreateSolidBrush(Background);
        state->sharpness = CreateWindowExW(0,TRACKBAR_CLASSW,L"",WS_CHILD|WS_VISIBLE|WS_TABSTOP|TBS_NOTICKS,
            190,405,520,25,window,reinterpret_cast<HMENU>(101),nullptr,nullptr);
        state->sky = CreateWindowExW(0,TRACKBAR_CLASSW,L"",WS_CHILD|WS_VISIBLE|WS_TABSTOP|TBS_NOTICKS,
            190,460,520,25,window,reinterpret_cast<HMENU>(102),nullptr,nullptr);
        SendMessageW(state->sharpness,TBM_SETRANGE,TRUE,MAKELPARAM(0,1000));
        SendMessageW(state->sky,TBM_SETRANGE,TRUE,MAKELPARAM(0,5000));
        SendMessageW(state->sky,TBM_SETPOS,TRUE,1000);
        return 0;
    }
    case WM_ERASEBKGND: return 1;
    case WM_CTLCOLORSTATIC:
        if (state) { SetBkColor(reinterpret_cast<HDC>(wp),Background); return reinterpret_cast<LRESULT>(state->background); }
        break;
    case WM_HSCROLL:
        InvalidateRect(window,nullptr,FALSE);
        return 0;
    case WM_LBUTTONUP: {
        if (!state) break;
        int x = LOWORD(lp), y = HIWORD(lp);
        if (x < 160 && y >= 55) {
            int tab = (y - 55) / 37;
            if (tab < static_cast<int>(Tabs.size())) {
                state->tab = tab;
                ShowWindow(state->sharpness,tab == 0 ? SW_SHOW : SW_HIDE);
                ShowWindow(state->sky,tab == 0 ? SW_SHOW : SW_HIDE);
            }
        } else if (state->tab == 0 && x >= 190 && x < 710 && y >= 85 && y < 385) {
            int column = x >= 450 ? 1 : 0;
            int row = (y - 85) / 30;
            int index = row * 2 + column;
            if (index < static_cast<int>(Options.size())) state->enabled[index] = !state->enabled[index];
        }
        InvalidateRect(window,nullptr,FALSE);
        return 0;
    }
    case WM_PAINT: {
        PAINTSTRUCT paint;
        HDC dc = BeginPaint(window,&paint);
        RECT bounds; GetClientRect(window,&bounds);
        HDC memory = CreateCompatibleDC(dc);
        HBITMAP bitmap = CreateCompatibleBitmap(dc,bounds.right,bounds.bottom);
        HGDIOBJ oldBitmap = SelectObject(memory,bitmap);
        HGDIOBJ oldFont = SelectObject(memory,state->font);
        SetBkMode(memory,TRANSPARENT);
        Fill(memory,bounds,Background);
        Fill(memory,{0,40,160,bounds.bottom},RGB(32,32,39));
        Text(memory,L"SDDS CHEATS",{0,0,bounds.right,40},RGB(230,230,238),DT_CENTER);
        Fill(memory,{180,55,720,56},RGB(38,117,177));
        Text(memory,L"PREVIA NATIVA",{570,24,720,42},RGB(125,125,139),DT_RIGHT);
        for (int i=0;i<static_cast<int>(Tabs.size());++i) {
            int y=55+i*37;
            if (i==state->tab) { Fill(memory,{10,y,150,y+30},RGB(42,42,54)); Fill(memory,{10,y,12,y+30},Accent); }
            Text(memory,Tabs[i],{28,y,150,y+30},i==state->tab?RGB(235,235,240):RGB(135,135,150));
        }
        Text(memory,Tabs[state->tab],{190,62,450,82},RGB(210,210,220));
        if (state->tab==0) {
            for (int i=0;i<static_cast<int>(Options.size());++i) {
                int x=190+(i%2)*260,y=85+(i/2)*30;
                HBRUSH track=CreateSolidBrush(state->enabled[i]?Accent:RGB(38,59,87));
                HGDIOBJ previous=SelectObject(memory,track);
                HGDIOBJ previousPen=SelectObject(memory,GetStockObject(NULL_PEN));
                RoundRect(memory,x,y+6,x+30,y+22,16,16);
                SelectObject(memory,GetStockObject(WHITE_BRUSH));
                int knob=x+(state->enabled[i]?14:0);
                Ellipse(memory,knob,y+6,knob+16,y+22);
                SelectObject(memory,previousPen);SelectObject(memory,previous);DeleteObject(track);
                Text(memory,Options[i],{x+40,y,x+250,y+29},RGB(150,150,164));
            }
            wchar_t value[32];
            Text(memory,L"Sharpness",{190,384,400,405},RGB(210,210,220));
            swprintf_s(value,L"%.3f",SendMessageW(state->sharpness,TBM_GETPOS,0,0)/1000.0);
            Text(memory,value,{600,384,710,405},RGB(170,170,185),DT_RIGHT);
            Text(memory,L"Sky Scale",{190,440,400,460},RGB(210,210,220));
            swprintf_s(value,L"%.3f",SendMessageW(state->sky,TBM_GETPOS,0,0)/1000.0);
            Text(memory,value,{600,440,710,460},RGB(170,170,185),DT_RIGHT);
        } else {
            Text(memory,L"Secao sem integracao com o jogo.",{190,110,710,145},RGB(155,155,170));
        }
        Text(memory,L"Controles demonstrativos. Nenhuma memoria do jogo e alterada.",{190,505,730,535},RGB(120,120,136));
        BitBlt(dc,0,0,bounds.right,bounds.bottom,memory,0,0,SRCCOPY);
        SelectObject(memory,oldFont);SelectObject(memory,oldBitmap);
        DeleteObject(bitmap);DeleteDC(memory);EndPaint(window,&paint);
        return 0;
    }
    case WM_DESTROY: return 0;
    case WM_NCDESTROY:
        if (state) { DeleteObject(state->font);DeleteObject(state->background);delete state;SetWindowLongPtrW(window,GWLP_USERDATA,0); }
        break;
    }
    return DefWindowProcW(window,message,wp,lp);
}
}

HWND WINAPI SddsCreateMenu() {
    HMODULE module = nullptr;
    if (!GetModuleHandleExW(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS|GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,
        reinterpret_cast<LPCWSTR>(&SddsCreateMenu),&module)) return nullptr;
    INITCOMMONCONTROLSEX controls{sizeof(controls),ICC_BAR_CLASSES};
    InitCommonControlsEx(&controls);
    WNDCLASSEXW wc{};wc.cbSize=sizeof(wc);wc.lpfnWndProc=Procedure;
    wc.hInstance=module;wc.lpszClassName=ClassName;wc.hCursor=LoadCursorW(nullptr,IDC_ARROW);
    if (!RegisterClassExW(&wc) && GetLastError()!=ERROR_CLASS_ALREADY_EXISTS) return nullptr;
    RECT size{0,0,750,550};
    DWORD style=WS_OVERLAPPED|WS_CAPTION|WS_SYSMENU|WS_MINIMIZEBOX|WS_CLIPCHILDREN;
    AdjustWindowRect(&size,style,FALSE);
    return CreateWindowExW(0,ClassName,L"Sdds cheats - Menu nativo",style|WS_VISIBLE,
        CW_USEDEFAULT,CW_USEDEFAULT,size.right-size.left,size.bottom-size.top,nullptr,nullptr,module,nullptr);
}

void WINAPI SddsDestroyMenu(HWND window) { if (IsWindow(window)) DestroyWindow(window); }
