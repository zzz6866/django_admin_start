import sys
from ctypes import *

from namuh_bot.models import *
from namuh_bot.namuh_windows import WinDllWmca

kernel32 = windll.kernel32
user32 = windll.user32
gdi32 = windll.gdi32

NULL = 0
CW_USEDEFAULT = -2147483648
IDI_APPLICATION = 32512
WS_OVERLAPPEDWINDOW = 13565952

CS_HREDRAW = 2
CS_VREDRAW = 1

IDC_ARROW = 32512
WHITE_BRUSH = 0

SW_SHOWNORMAL = 1

WNDPROC = WINFUNCTYPE(c_long, c_int, c_uint, c_int, c_int)


class WNDCLASS(Structure):
    _fields_ = [('style', c_uint),
                ('lpfnWndProc', WNDPROC),
                ('cbClsExtra', c_int),
                ('cbWndExtra', c_int),
                ('hInstance', c_int),
                ('hIcon', c_int),
                ('hCursor', c_int),
                ('hbrBackground', c_int),
                ('lpszMenuName', c_char_p),
                ('lpszClassName', c_char_p)]


class RECT(Structure):
    _fields_ = [('left', c_long),
                ('top', c_long),
                ('right', c_long),
                ('bottom', c_long)]


class PAINTSTRUCT(Structure):
    _fields_ = [('hdc', c_int),
                ('fErase', c_int),
                ('rcPaint', RECT),
                ('fRestore', c_int),
                ('fIncUpdate', c_int),
                ('rgbReserved', c_char * 32)]


class POINT(Structure):
    _fields_ = [('x', c_long),
                ('y', c_long)]


class MSG(Structure):
    _fields_ = [('hwnd', c_int),
                ('message', c_uint),
                ('wParam', c_int),
                ('lParam', c_int),
                ('time', c_int),
                ('pt', POINT)]


def ErrorIfZero(handle):
    if handle == 0:
        raise WinError
    else:
        return handle


def MainWin():
    global NULL
    CreateWindowEx = user32.CreateWindowExA
    CreateWindowEx.argtypes = [c_int, c_char_p, c_char_p, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_int, c_int]
    CreateWindowEx.restype = ErrorIfZero

    # Define Window Class
    wndclass = WNDCLASS()
    wndclass.style = CS_HREDRAW | CS_VREDRAW
    wndclass.lpfnWndProc = WNDPROC(WndProc)
    wndclass.cbClsExtra = wndclass.cbWndExtra = 0
    wndclass.hInstance = kernel32.GetModuleHandleA(c_int(NULL))
    wndclass.hIcon = user32.LoadIconA(c_int(NULL), c_int(IDI_APPLICATION))
    wndclass.hCursor = user32.LoadCursorA(c_int(NULL), c_int(IDC_ARROW))
    wndclass.hbrBackground = gdi32.GetStockObject(c_int(WHITE_BRUSH))
    wndclass.lpszMenuName = None
    wndclass.lpszClassName = b"MainWin"
    # Register Window Class
    if not user32.RegisterClassA(byref(wndclass)):
        raise WinError()
    # Create Window
    hwnd = CreateWindowEx(0,
                          wndclass.lpszClassName,
                          b"Python Window",
                          WS_OVERLAPPEDWINDOW,
                          CW_USEDEFAULT,
                          CW_USEDEFAULT,
                          CW_USEDEFAULT,
                          CW_USEDEFAULT,
                          NULL,
                          NULL,
                          wndclass.hInstance,
                          NULL)

    # Show Window
    user32.ShowWindow(c_int(hwnd), c_int(SW_SHOWNORMAL))
    user32.UpdateWindow(c_int(hwnd))

    wmca = WinDllWmca()
    wmca.connect(hwnd)  # 프로그램 실행시 로그인

    # Pump Messages
    msg = MSG()
    pMsg = pointer(msg)
    NULL = c_int(NULL)

    while user32.GetMessageA(pMsg, NULL, 0, 0) != 0:
        user32.TranslateMessage(pMsg)
        user32.DispatchMessageA(pMsg)

    return msg.wParam


WM_PAINT = 15
WM_DESTROY = 2

DT_SINGLELINE = 32
DT_CENTER = 1
DT_VCENTER = 4


def WndProc(hwnd, message, wParam, lParam):
    ps = PAINTSTRUCT()
    rect = RECT()

    if message == WM_PAINT:
        hdc = user32.BeginPaint(c_int(hwnd), byref(ps))
        user32.GetClientRect(c_int(hwnd), byref(rect))
        user32.DrawTextA(c_int(hdc),
                         b"Python Powered Windows",
                         c_int(-1), byref(rect),
                         DT_SINGLELINE | DT_CENTER | DT_VCENTER)
        user32.EndPaint(c_int(hwnd), byref(ps))
        return 0
    elif message == WM_DESTROY:
        user32.PostQuitMessage(0)
        return 0
    elif wParam == CA_CONNECTED:  # 로그인 성공
        print("로그인 성공")
    elif wParam == CA_DISCONNECTED:  # 접속 끊김
        print("접속 끊김")
    elif wParam == CA_SOCKETERROR:  # 통신 오류 발생
        print("통신 오류 발생")
    elif wParam == CA_RECEIVEDATA:  # 서비스 응답 수신(TR)
        print("서비스 응답 수신(TR)")
    elif wParam == CA_RECEIVESISE:  # 실시간 데이터 수신(BC)
        print("실시간 데이터 수신(BC)")
    elif wParam == CA_RECEIVEMESSAGE:  # 상태 메시지 수신 (입력값이 잘못되었을 경우 문자열형태로 설명이 수신됨)
        print("상태 메시지 수신 (입력값이 잘못되었을 경우 문자열형태로 설명이 수신됨)")
    elif wParam == CA_RECEIVECOMPLETE:  # 서비스 처리 완료
        print("서비스 처리 완료")
    elif wParam == CA_RECEIVEERROR:  # 서비스 처리중 오류 발생 (입력값 오류등)
        print("서비스 처리중 오류 발생 (입력값 오류등)")

    return user32.DefWindowProcA(c_int(hwnd), c_int(message), c_int(wParam), c_int(lParam))


if __name__ == '__main__':
    sys.exit(MainWin())
