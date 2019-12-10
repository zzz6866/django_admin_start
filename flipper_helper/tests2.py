#!python3

import os
import sys
import tkinter as tk
from sys import platform

from alldev.settings.base import BASE_DIR

if any([platform.startswith(os_name) for os_name in ['linux', 'darwin', 'freebsd']]):  # 리눅스용
    import zugbruecke as ctypes
    import zugbruecke.wintypes as wintypes
elif platform.startswith('win'):  # 윈도우용
    import ctypes
    import ctypes.wintypes as wintypes

    os.environ['PATH'] = ';'.join([os.environ['PATH'], BASE_DIR + r"\flipper_helper\bin"])
else:
    # Handle unsupported platforms
    print("NOT USEABLE")
from threading import Thread


class FlipperHelperMynamuh():
    def __init__(self):
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32
        self.wmca_dll = ctypes.WinDLL('wmca.dll')
        self.WM_TEST = 0x24D0
        self.tid = self.kernel32.GetCurrentThreadId()
        self.hWnd = wintypes.HWND()
        self.msg = wintypes.MSG()

    def PostThreadMessage(self):
        self.user32.PostThreadMessageW(self.tid, self.WM_TEST, 0, 0)

    def wmcaConnect(self):
        INPUT_PARM, OUTPUT_PARAM, INPUT_PARM_DEFAULT_ZERO = 1, 2, 4

        msg = self.WM_TEST
        sz_id = b"start0"
        sz_pw = b"qpwoei12!@"
        sz_cert_pw = b"ekdnsfhem1!"

        prototype = ctypes.WINFUNCTYPE(wintypes.INT, wintypes.HWND, wintypes.DWORD, wintypes.CHAR, wintypes.CHAR, wintypes.LPSTR, wintypes.LPSTR, wintypes.LPSTR)
        paramflags = ((INPUT_PARM, "hWnd", self.hWnd),
                      (INPUT_PARM, "msg", msg),
                      (INPUT_PARM, "MediaType", b"T"),
                      (INPUT_PARM, "UserType", b"W"),
                      (INPUT_PARM, "szID", sz_id),
                      (INPUT_PARM, "szPW", sz_pw),
                      (INPUT_PARM, "szCertPW", sz_cert_pw))
        connect = prototype(("wmcaConnect", self.wmca_dll), paramflags)
        result = connect()

        print("result : ", result)
        print("wmcaIsConnected : ", self.wmca_dll.wmcaIsConnected())

    def callback(self, dwMessageType, lParam):
        print(dwMessageType)
        print(lParam)

    def wmcaLoad(self):
        wmca_dll = ctypes.WinDLL('wmca.dll')
        wmcaLoad = wmca_dll.wmcaLoad
        result = wmcaLoad()
        print("wmcaLoad : ", result)

    def wmcaFree(self):
        wmca_dll = ctypes.WinDLL('wmca.dll')
        wmcaFree = wmca_dll.wmcaFree
        result = wmcaFree()
        print("wmcaFree : ", result)

    def wmcaSetPort(self):
        wmcaSetPort = self.wmca_dll.wmcaSetPort
        result = wmcaSetPort(8400)
        print("wmcaSetPort : ", result)

    def wmcaDetachAll(self):
        wmcaDetachAll = self.wmca_dll.wmcaDetachAll
        result = wmcaDetachAll()
        print("wmcaDetachAll : ", result)

    def wmcaDisconnect(self):
        wmcaDisconnect = self.wmca_dll.wmcaDisconnect
        result = wmcaDisconnect()
        print("wmcaDisconnect : ", result)

    """
    
    class Callback(ctypes.Structure):
        _fields_ = [
            ("dwMessageType", wintypes.WPARAM),
            ("lParam", wintypes.LPARAM)
        ]
    """

    def setWinEventHook(self):
        WinEventProcType = ctypes.WINFUNCTYPE(
            None,
            wintypes.WPARAM,
            wintypes.LPARAM
        )
        WinEventProc = WinEventProcType(self.callback)
        self.user32.SetWinEventHook.restype = ctypes.wintypes.HANDLE
        hook = self.user32.SetWinEventHook(
            self.WM_TEST,
            self.WM_TEST,
            0,
            WinEventProc,
            0,
            0,
            0
        )
        print("setWinEventHook success")


flipper_nm = FlipperHelperMynamuh()

root = tk.Tk()

t = Thread(target=flipper_nm.__init__)
t.daemon = True
t.start()

tk.Button(root, text='----------------------------------------------------------------------------').pack()
tk.Button(root, text='PostThreadMessage', command=flipper_nm.PostThreadMessage).pack()
tk.Button(root, text='로그인', command=flipper_nm.wmcaConnect).pack()
tk.Button(root, text='로그아웃', command=flipper_nm.wmcaDisconnect).pack()
tk.Button(root, text='후킹', command=flipper_nm.setWinEventHook).pack()
tk.Button(root, text='dll 로드', command=flipper_nm.wmcaLoad).pack()
tk.Button(root, text='dll 종료', command=flipper_nm.wmcaFree).pack()
tk.Button(root, text='port 설정', command=flipper_nm.wmcaSetPort).pack()
tk.Button(root, text='주문 취소', command=flipper_nm.wmcaDetachAll).pack()

root.mainloop()
