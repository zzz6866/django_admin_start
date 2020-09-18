import sys

import win32api
import win32con
import win32gui
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

import os

from namuh_bot.models import *
from alldev.settings.base import BASE_DIR

from ctypes.wintypes import *
os.environ['PATH'] = ';'.join([os.environ['PATH'], BASE_DIR + r"\namuh_bot\bin"])



# Create your tests here.


class NamuhWindow:
    def __init__(self):
        # message map
        message_map = {
            # msg_TaskbarRestart: self.OnRestart,
            # win32con.WM_DESTROY: self.OnDestroy,
            win32con.WM_COMMAND: self.wnd_proc,
            ON_TASKBAR_NOTIFY: self.on_taskbar_notify,
        }

        # Define Window Class
        wc = win32gui.WNDCLASS()
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        wc.lpfnWndProc = message_map
        wc.hInstance = win32gui.GetModuleHandle(None)
        wc.hIcon = win32gui.LoadIcon(None, IDI_APPLICATION)
        wc.hCursor = win32gui.LoadCursor(None, IDC_ARROW)
        wc.hbrBackground = win32gui.GetStockObject(WHITE_BRUSH)
        wc.lpszClassName = "MainWin"

        # Register Window Class
        if not win32gui.RegisterClass(wc):
            raise WinError()

        # Create Window
        self.hwnd = win32gui.CreateWindowEx(0,
                                            wc.lpszClassName,
                                            "Namuh Window",
                                            WS_OVERLAPPEDWINDOW,
                                            CW_USEDEFAULT,
                                            CW_USEDEFAULT,
                                            CW_USEDEFAULT,
                                            CW_USEDEFAULT,
                                            None,
                                            None,
                                            wc.hInstance,
                                            None)

        # Show Window
        # win32gui.ShowWindow(self.hwnd, SW_SHOWNORMAL)
        win32gui.UpdateWindow(self.hwnd)

        self._DoCreateIcons()  # 트레이 아이콘 생성

        self.wmca = WinDllWmca()  # 모바일증권 나무 DLL 로드
        win32gui.PumpMessages()  # MFC 메시지 수집

    def _DoCreateIcons(self):  # 트레이 아이콘 생성
        # Try and find a custom icon
        hinst = win32api.GetModuleHandle(None)
        iconPathName = os.path.abspath(os.path.join(os.path.split(sys.executable)[0], "pyc.ico"))
        if not os.path.isfile(iconPathName):
            # Look in DLLs dir, a-la py 2.5
            iconPathName = os.path.abspath(os.path.join(os.path.split(sys.executable)[0], "DLLs", "pyc.ico"))
        if not os.path.isfile(iconPathName):
            # Look in the source tree.
            iconPathName = os.path.abspath(os.path.join(os.path.split(sys.executable)[0], "..\\PC\\pyc.ico"))
        if os.path.isfile(iconPathName):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
        else:
            print("Can't find a Python icon file - using default")
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        nid = (self.hwnd, 0, flags, ON_TASKBAR_NOTIFY, hicon, "Namuh Tray")
        try:
            win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
        except win32gui.error as error:
            # This is common when windows is starting, and this code is hit
            # before the taskbar has been created.
            print("Failed to add the taskbar icon - is explorer running?", error)
            # but keep running anyway - when explorer starts, we get the
            # TaskbarCreated message.

    def wnd_proc(self, hwnd, message, wParam, lParam):
        if message == win32con.WM_DESTROY or wParam == MENU_EXIT or wParam == CA_DISCONNECTED:  # 윈도우 창 닫기 버튼 클릭시 # 접속 끊김
            print("Goodbye")
            win32gui.PostQuitMessage(0)
            win32gui.DestroyWindow(self.hwnd)
        elif wParam == CA_CONNECTED:  # 로그인 성공
            print("로그인 성공", lParam)
        elif wParam == CA_SOCKETERROR:  # 통신 오류 발생
            print("통신 오류 발생")
        elif wParam == CA_RECEIVEDATA:  # 서비스 응답 수신(TR)
            print("서비스 응답 수신(TR)")
        elif wParam == CA_RECEIVESISE:  # 실시간 데이터 수신(BC)
            print("실시간 데이터 수신(BC)")
        elif wParam == CA_RECEIVEMESSAGE:  # 상태 메시지 수신 (입력값이 잘못되었을 경우 문자열형태로 설명이 수신됨)
            self.on_wm_receivemessage(lParam)
        elif wParam == CA_RECEIVECOMPLETE:  # 서비스 처리 완료
            print("서비스 처리 완료")
        elif wParam == CA_RECEIVEERROR:  # 서비스 처리중 오류 발생 (입력값 오류등)
            print("서비스 처리중 오류 발생 (입력값 오류등)")

        return win32gui.DefWindowProc(hwnd, message, wParam, lParam)

    def on_wm_receivemessage(self, lparam):
        p_msg = cast(lparam, POINTER(OutdatablockStruct))
        p_msg_header = cast(p_msg.contents.pData.contents.szData, POINTER(MsgHeaderStruct))
        msg_cd = p_msg_header.contents.msg_cd.decode("utf-8")
        user_msg = p_msg_header.contents.user_msg.decode("euc-kr")
        print("상태 메시지 수신 (입력값이 잘못되었을 경우 문자열형태로 설명이 수신됨) = {1} : {2}".format(p_msg.contents.TrIndex, msg_cd, user_msg))

    def on_taskbar_notify(self, hwnd, msg, wparam, lparam):

        if lparam == win32con.WM_LBUTTONUP:
            print("You clicked me.")
        elif lparam == win32con.WM_LBUTTONDBLCLK:
            print("You double-clicked me - goodbye")
            win32gui.DestroyWindow(self.hwnd)
        elif lparam == win32con.WM_RBUTTONUP:
            print("You right clicked me.")
            menu = win32gui.CreatePopupMenu()
            # win32gui.AppendMenu(menu, win32con.MF_STRING, 1023, "Display Dialog")
            # win32gui.AppendMenu(menu, win32con.MF_STRING, 1024, "Say Hello")
            win32gui.AppendMenu(menu, win32con.MF_STRING, MENU_EXIT, "Exit program")
            pos = win32gui.GetCursorPos()
            # See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winui/menus_0hdi.asp
            win32gui.SetForegroundWindow(self.hwnd)
            win32gui.TrackPopupMenu(menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, self.hwnd, None)
            win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)
        return 1


class WinDllWmca:
    def __init__(self):
        self.wmca_dll = windll.LoadLibrary('wmca.dll')

    def connect(self, hwnd, sz_id, sz_pw, sz_cert_pw):  # 접속 후 로그인(인증)

        func = self.wmca_dll.wmcaConnect
        func.argtypes = [HWND, DWORD, CHAR, CHAR, LPSTR, LPSTR, LPSTR]
        func.restype = BOOL
        result = func(hwnd, CA_WMCAEVENT, b"T", b"W", sz_id, sz_pw, sz_cert_pw)
        print("connect =", bool(result))

    def disconnect(self):  # 접속 해제
        func = self.wmca_dll.wmcaDisconnect
        func.argtypes = []
        func.restype = BOOL
        result = func()
        print("disconnect =", bool(result))

    def is_connected(self):  # 접속 여부 확인
        func = self.wmca_dll.wmcaIsConnected
        func.argtypes = []
        func.restype = BOOL
        result = func()
        print("is_connected =", bool(result))

    def query(self, hwnd, szTRCode, szInput, nInputLen, nAccountIndex):  # 서비스(TR) 호출
        func = self.wmca_dll.wmcaQuery
        # HWND hWnd, int nTRID, constchar* szTRCode, const char* szInput, int nInputLen, int nAccountIndex
        func.argtypes = [HWND, INT, LPSTR, LPSTR, INT, INT]
        func.restype = BOOL
        result = func(hwnd, szTRCode, szInput, nInputLen, nAccountIndex)
        print("query =", bool(result))

    def attach(self, hwnd, szBCType, szInput, nCodeLen, nInputLen):  # 실시간 등록
        func = self.wmca_dll.wmcaQuery
        # HWND hWnd, const char* szBCType, const char* szInput, int nCodeLen, int nInputLen
        func.argtypes = [HWND, LPSTR, LPSTR, INT, INT]
        func.restype = BOOL
        result = func(hwnd, szBCType, szInput, nCodeLen, nInputLen)
        print("attach =", bool(result))

    def detach(self, hwnd, szBCType, szInput, nCodeLen, nInputLen):  # 실시간 취소
        func = self.wmca_dll.wmcaQuery
        # HWND hWnd, const char* szBCType, const char* szInput, int nCodeLen, int nInputLen
        func.argtypes = [HWND, LPSTR, LPSTR, INT, INT]
        func.restype = BOOL
        result = func(hwnd, szBCType, szInput, nCodeLen, nInputLen)
        print("detach =", bool(result))

    def detach_window(self, hwnd):  # 실시간 일괄 취소
        func = self.wmca_dll.wmcaDetachWindow
        func.argtypes = [HWND]
        func.restype = BOOL
        result = func(hwnd)
        print("detach_window =", bool(result))

    def detach_all(self):  # 실시간 일괄 취소
        func = self.wmca_dll.wmcaDetachAll
        func.argtypes = []
        func.restype = BOOL
        result = func()
        print("detach_all =", bool(result))

    def load(self):  # dll 실행
        func = self.wmca_dll.wmcaLoad
        func.argtypes = []
        func.restype = BOOL
        result = func()
        print("load =", bool(result))

    def free(self):  # dll 종료
        func = self.wmca_dll.wmcaFree
        func.argtypes = []
        func.restype = BOOL
        result = func()
        print("free =", bool(result))


if __name__ == '__main__':
    w = NamuhWindow()
