#!python3

import os
import sys
import tkinter as tk
from sys import platform

from alldev.settings.base import BASE_DIR

if any([platform.startswith(os_name) for os_name in ['linux', 'darwin', 'freebsd']]):  # 리눅스용
    from zugbruecke import *
    from zugbruecke.wintypes import *
elif platform.startswith('win'):  # 윈도우용
    from ctypes import *
    from wintypes import *

    os.environ['PATH'] = ';'.join([os.environ['PATH'], BASE_DIR + r"\flipper_helper\bin"])
else:
    # Handle unsupported platforms
    print("NOT USEABLE")
from threading import Thread

ULONG_PTR = WPARAM
LRESULT = LPARAM
LPMSG = POINTER(MSG)

HOOKPROC = WINFUNCTYPE(LRESULT, INT, WPARAM, LPARAM)
WmcaEventProc = HOOKPROC


class WMCAHOOKSTRUCT(Structure):
    _fields_ = (('wParam', WPARAM),
                ('lParam ', LPARAM))


LPMSLLHOOKSTRUCT = POINTER(WMCAHOOKSTRUCT)


def errcheck_bool(result, func, args):
    if not result:
        raise WinError(get_last_error())
    return args


class FlipperHelperMynamuh():
    def __init__(self):
        self.user32 = windll.user32
        self.kernel32 = windll.kernel32
        self.wmca_dll = WinDLL('wmca.dll')
        self.WM_WMCA_EVENT = 0x24D0
        self.tid = self.kernel32.GetCurrentThreadId()
        self.hWnd = HWND()
        self.msg = MSG()

    def SendMessage(self):
        print("SendMessage")


flipper_nm = FlipperHelperMynamuh()

root = tk.Tk()

t = Thread(target=flipper_nm.__init__)
t.daemon = True
t.start()

tk.Button(root, text='----------------------------------------------------------------------------').pack()
tk.Button(root, text='SendMessage', command=flipper_nm.SendMessage).pack()

root.mainloop()
