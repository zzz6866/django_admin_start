#!python3

import os
import time
import tkinter as tk
from sys import platform

from alldev.settings.base import BASE_DIR

if any([platform.startswith(os_name) for os_name in ['linux', 'darwin', 'freebsd']]):  # 리눅스용
    from zugbruecke import *
    from zugbruecke.wintypes import *
elif platform.startswith('win'):  # 윈도우용
    from ctypes import *
    from ctypes.wintypes import *

    os.environ['PATH'] = ';'.join([os.environ['PATH'], BASE_DIR + r"\flipper_helper\bin"])
    print(os.environ['PATH'].split(";"))
else:
    # Handle unsupported platforms
    print("NOT USEABLE")
from threading import Thread


class CWPRETSTRUCT(Structure):
    ''' a class to represent CWPRETSTRUCT structure
    https://msdn.microsoft.com/en-us/library/windows/desktop/ms644963(v=vs.85).aspx '''

    _fields_ = [('lResult', LPARAM),
                ('lParam', LPARAM),
                ('wParam', WPARAM),
                ('message', UINT),
                ('hwnd', HWND)]


class WINDOWPOS(Structure):
    ''' a class to represent WINDOWPOS structure
    https://msdn.microsoft.com/en-gb/library/windows/desktop/ms632612(v=vs.85).aspx '''

    _fields_ = [('hwnd', HWND),
                ('hwndInsertAfter', HWND),
                ('x', INT),
                ('y', INT),
                ('cx', INT),
                ('cy', INT),
                ('flags', UINT)]


class App(tk.Tk):
    ''' generic tk app with win api interaction '''

    wh_callwndprocret = 12
    wh_callwndproc = 4
    wh_getmessage = 3
    wh_journalrecord = 0
    wh_journalplayback = 1
    wh_keyboard = 2
    wh_cbt = 5
    wh_sysmsgfilter = 6

    wm_windowposchanged = 71

    swp_noownerzorder = 512
    set_hook = windll.user32.SetWindowsHookExW
    call_next_hook = windll.user32.CallNextHookEx
    un_hook = windll.user32.UnhookWindowsHookEx
    get_thread = windll.kernel32.GetCurrentThreadId
    get_error = windll.kernel32.GetLastError
    get_parent = windll.user32.GetParent
    wnd_ret_proc = WINFUNCTYPE(c_long, INT, WPARAM, LPARAM)
    wmca_dll = WinDLL('wmca.dll', use_last_error=True)

    register_window_message = windll.user32.RegisterWindowMessageW
    CA_WMCAEVENT = register_window_message("CA_WMCAEVENT")
    CA_CONNECTED = register_window_message("CA_CONNECTED")
    CA_DISCONNECTED = register_window_message("CA_DISCONNECTED")
    CA_SOCKETERROR = register_window_message("CA_SOCKETERROR")
    CA_RECEIVEDATA = register_window_message("CA_RECEIVEDATA")
    CA_RECEIVESISE = register_window_message("CA_RECEIVESISE")
    CA_RECEIVEMESSAGE = register_window_message("CA_RECEIVEMESSAGE")
    CA_RECEIVECOMPLETE = register_window_message("CA_RECEIVECOMPLETE")
    CA_RECEIVEERROR = register_window_message("CA_RECEIVEERROR")

    def __init__(self):
        ''' generic __init__ '''

        super().__init__()
        self.minsize(700, 400)
        self.hook = self.setup_hook()
        self.protocol('WM_DELETE_WINDOW', self.on_closing)

    def setup_hook(self):
        ''' setting up the hook '''

        thread = self.get_thread()
        hook = self.set_hook(self.wh_callwndprocret, self.call_wnd_ret_proc, HINSTANCE(0), thread)
        hook = self.set_hook(self.wh_callwndproc, self.call_wnd_ret_proc, HINSTANCE(0), thread)

        if not hook:
            raise WinError(self.get_error())

        return hook

    def on_closing(self):
        ''' releasing the hook '''
        if self.hook:
            self.un_hook(self.hook)
        self.destroy()

    @staticmethod
    @wnd_ret_proc
    def call_wnd_ret_proc(nCode, wParam, lParam):
        ''' an implementation of the CallWndRetProc callback
        https://msdn.microsoft.com/en-us/library/windows/desktop/ms644976(v=vs.85).aspx'''

        #   get a message
        msg = cast(lParam, POINTER(CWPRETSTRUCT)).contents
        if msg.message == App.wm_windowposchanged and msg.hwnd == App.get_parent(app.winfo_id()):
            #   if message, which belongs to owner hwnd, is signaling that windows position is changed - check z-order
            wnd_pos = cast(msg.lParam, POINTER(WINDOWPOS)).contents
            print('z-order changed: %r' % ((wnd_pos.flags & App.swp_noownerzorder) != App.swp_noownerzorder))
        elif msg.message == App.CA_WMCAEVENT and msg.hwnd == App.get_parent(app.winfo_id()):
            print("CA_WMCAEVENT")
        elif msg.message == App.CA_WMCAEVENT:
            print("CA_WMCAEVENT")

        return App.call_next_hook(None, nCode, wParam, lParam)

    def send_message(self):
        result = windll.user32.PostMessageW(HINSTANCE(0), App.CA_WMCAEVENT, 1, 1)
        print(result)
        result = windll.user32.SendMessageW(HINSTANCE(0), App.CA_WMCAEVENT, 1, 1)
        print(result)
        result = windll.user32.PostMessageW(HINSTANCE(0), App.wm_windowposchanged, 1, 1)
        print(result)
        result = windll.user32.SendMessageW(HINSTANCE(0), App.wm_windowposchanged, 1, 1)
        print(result)

    def wmcaConnect(self):
        INPUT_PARM, OUTPUT_PARAM, INPUT_PARM_DEFAULT_ZERO = 1, 2, 4

        msg = self.CA_WMCAEVENT
        sz_id = b"start0"
        sz_pw = b"qpwoei12!@"
        sz_cert_pw = b"ekdnsfhem1!"

        wmcaConnect = self.wmca_dll.wmcaConnect
        wmcaConnect.argtypes = [HWND, DWORD, CHAR, CHAR, LPSTR, LPSTR, LPSTR]
        wmcaConnect.restype = BOOL
        # wmcaConnect.errcheck = errcheck
        result = wmcaConnect(HINSTANCE(0), msg, b'T', b'W', sz_id, sz_pw, sz_cert_pw)

        print("result : ", result)
        print("wmcaIsConnected : ", self.wmca_dll.wmcaIsConnected())


app = App()

tk.Button(app, text='SendMessage', command=app.send_message).pack()
tk.Button(app, text='wmcaConnect', command=app.wmcaConnect).pack()

app.mainloop()
