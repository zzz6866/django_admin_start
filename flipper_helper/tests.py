from ctypes import c_char, byref

from django.test import TestCase

# Create your tests here.
from zugbruecke import WINFUNCTYPE, cdll

if __name__ == "__main__":
    import zugbruecke as ctypes
    from zugbruecke import POINTER, WINFUNCTYPE, windll, WinError, c_char_p, cast
    from zugbruecke.wintypes import BOOL, HWND, RECT, INT, DWORD, CHAR, PCHAR, LPCWSTR, UINT, PDWORD, LPSTR

    hWnd = HWND(0)
    msg = DWORD(0)
    sz_id = c_char_p(b"aaaaa")
    sz_pw = c_char_p(b"aaaaaa")
    sz_cert_pw = c_char_p(b"aaaaaa")

    INPUT_PARM, OUTPUT_PARAM, INPUT_PARM_DEFAULT_ZERO = 1, 2, 4

    # wmca_dll = ctypes.windll.LoadLibrary('wmca.dll')
    wmca_dll = ctypes.WinDLL('wmca.dll')
    wmcaConnect = wmca_dll.wmcaConnect
    wmcaConnect.argtypes = [POINTER(HWND), PDWORD, CHAR, CHAR, LPSTR, LPSTR, LPSTR]
    wmcaConnect.restype = BOOL

    print(wmcaConnect(byref(hWnd), byref(msg), b'T', b'W', sz_id, sz_pw, sz_cert_pw))
    print("pointer : ", hWnd.value, msg.value)
    # print("wmcaDisconnect : ", wmca_dll.wmcaDisconnect())

    # property_func = WINFUNCTYPE(HWND, DWORD, CHAR, CHAR, LPSTR, LPSTR, LPSTR)
    # result = property_func(wmcaConnect(byref(hWnd), byref(msg), b'T', b'W', sz_id, sz_pw, sz_cert_pw))
    # print("result : ", result)
    # print("pointer : ", hWnd.value, msg.value)
    # del wmca_dll
    """prototype = WINFUNCTYPE(HWND, DWORD, CHAR, CHAR, PCHAR, PCHAR, PCHAR)
    paramflags = ((OUTPUT_PARAM, "hWnd", hWnd),
                  (OUTPUT_PARAM, "msg", msg),
                  (INPUT_PARM, "MediaType", "T"),
                  (INPUT_PARM, "UserType", "W"),
                  (INPUT_PARM, "szID", sz_id),
                  (INPUT_PARM, "szPW", sz_pw),
                  (INPUT_PARM, "szCertPW", sz_cert_pw))
    connect = prototype(("wmcaConnect", wmca), paramflags)"""

    """INPUT_PARM, OUTPUT_PARAM, INPUT_PARM_DEFAULT_ZERO = 1, 2, 4
    prototype = WINFUNCTYPE(INT, HWND, LPCWSTR, LPCWSTR, UINT)
    paramflags = ((INPUT_PARM, "hwnd", 0),
                  (INPUT_PARM, "text", "Hi"),
                  (INPUT_PARM, "caption", "Your title"),
                  (INPUT_PARM, "flags", MB_HELP | MB_YESNO | ICON_STOP))
    MessageBox = prototype(("MessageBoxA", windll.user32), paramflags)

    MessageBox()
    MessageBox(text="Spam, spam, spam")
    MessageBox(flags=1, text="foo bar")"""

    """libc = cdll.msvcrt
    strchr = libc.strchr
    strchr.restype = c_char_p
    strchr.argtypes = [c_char_p, c_char]
    strchr(b"abcdef", b"d")

    strchr(b"abcdef", b"def")

    print(strchr(b"abcdef", b"x"))

    strchr(b"abcdef", b"d")"""
