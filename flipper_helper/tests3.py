from ctypes import *
from ctypes.wintypes import *

user32 = WinDLL('user32', use_last_error=True)

HC_ACTION = 0
WH_CALLWNDPROC = 4
WH_MOUSE_LL = 14
WM_WMCA_EVENT = 0x24D0
WM_QUIT = 0x0012

MSG_TEXT = {WM_WMCA_EVENT: 'WM_WMCA_EVENT'}

ULONG_PTR = WPARAM
LRESULT = LPARAM
LPMSG = POINTER(MSG)

HOOKPROC = WINFUNCTYPE(LRESULT, c_int, WPARAM, LPARAM)
CallWndProc = HOOKPROC


class tagCWPSTRUCT(Structure):
    _fields_ = (('lParam ', LPARAM),
                ('wParam', WPARAM),
                ('message', UINT),
                ('hwnd', HWND))


LPMSLLHOOKSTRUCT = POINTER(tagCWPSTRUCT)


def errcheck_bool(result, func, args):
    if not result:
        raise WinError(get_last_error())
    return args


user32.SetWindowsHookExW.errcheck = errcheck_bool
user32.SetWindowsHookExW.restype = HHOOK
user32.SetWindowsHookExW.argtypes = (c_int,  # _In_ idHook
                                     HOOKPROC,  # _In_ lpfn
                                     HINSTANCE,  # _In_ hMod
                                     DWORD)  # _In_ dwThreadId

user32.CallNextHookEx.restype = LRESULT
user32.CallNextHookEx.argtypes = (HHOOK,  # _In_opt_ hhk
                                  c_int,  # _In_     nCode
                                  WPARAM,  # _In_     wParam
                                  LPARAM)  # _In_     lParam

user32.GetMessageW.argtypes = (LPMSG,  # _Out_    lpMsg
                               HWND,  # _In_opt_ hWnd
                               UINT,  # _In_     wMsgFilterMin
                               UINT)  # _In_     wMsgFilterMax

user32.TranslateMessage.argtypes = (LPMSG,)
user32.DispatchMessageW.argtypes = (LPMSG,)


@CallWndProc
def CallbackFunc(nCode, wParam, lParam):
    return user32.CallNextHookEx(None, nCode, wParam, lParam)


def mouse_msg_loop():
    hHook = user32.SetWindowsHookExW(WH_CALLWNDPROC, CallbackFunc, None, 0)
    msg = MSG()
    while True:
        bRet = user32.GetMessageW(byref(msg), None, 0, 0)
        if not bRet:
            break
        if bRet == -1:
            raise WinError(get_last_error())
        user32.TranslateMessage(byref(msg))
        user32.DispatchMessageW(byref(msg))


if __name__ == '__main__':
    import time
    import threading

    t = threading.Thread(target=mouse_msg_loop)
    t.start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            user32.PostThreadMessageW(t.ident, WM_QUIT, 0, 0)
            break
