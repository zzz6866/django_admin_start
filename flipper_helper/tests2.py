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

    os.environ['PATH'] = ''.join([os.environ['PATH'], BASE_DIR + r"\flipper_helper\bin"])
else:
    # Handle unsupported platforms
    print("NOT USEABLE")
from threading import Thread

WM_USER = 1024
CA_WMCAEVENT = WM_USER + 8400
CA_CONNECTED = WM_USER + 110
CA_DISCONNECTED = WM_USER + 120
CA_SOCKETERROR = WM_USER + 130
CA_RECEIVEDATA = WM_USER + 210
CA_RECEIVESISE = WM_USER + 220
CA_RECEIVEMESSAGE = WM_USER + 230
CA_RECEIVECOMPLETE = WM_USER + 240
CA_RECEIVEERROR = WM_USER + 250


class FlipperHelperMynamuh():
    def __init__(self):
        self.user32 = WinDLL('user32', use_last_error=True)
        self.kernel32 = ctypes.windll.kernel32
        self.wmca_dll = ctypes.WinDLL('wmca.dll')
        self.WM_WMCA_EVENT = 9424

        self.tid = self.kernel32.GetCurrentThreadId()
        self.hWnd = HWND()
        self.msg = MSG()

    def SendMessage(self):
        self.user32.SendMessageW(self.wmca_dll._handle, self.WM_WMCA_EVENT, 11111, 11111)

    def wmcaConnect(self):
        INPUT_PARM, OUTPUT_PARAM, INPUT_PARM_DEFAULT_ZERO = 1, 2, 4

        msg = self.WM_WMCA_EVENT
        sz_id = b"start0"
        sz_pw = b"qpwoei12!@"
        sz_cert_pw = b"ekdnsfhem1!"

        wmcaConnect = self.wmca_dll.wmcaConnect
        wmcaConnect.argtypes = [HWND, DWORD, CHAR, CHAR, LPSTR, LPSTR, LPSTR]
        wmcaConnect.restype = BOOL
        # wmcaConnect.errcheck = errcheck
        result = wmcaConnect(self.hWnd, msg, b'T', b'W', sz_id, sz_pw, sz_cert_pw)

        print("result : ", result)
        print("wmcaIsConnected : ", self.wmca_dll.wmcaIsConnected())

    def setHook(self):

        HC_ACTION = 0
        WH_CALLWNDPROC = 4
        WH_MOUSE_LL = 14
        WM_QUIT = 0x0012

        MSG_TEXT = {self.WM_WMCA_EVENT: 'WM_WMCA_EVENT'}

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

        self.user32.SetWindowsHookExW.errcheck = errcheck_bool
        self.user32.SetWindowsHookExW.restype = HHOOK
        self.user32.SetWindowsHookExW.argtypes = (c_int,  # _In_ idHook
                                                  HOOKPROC,  # _In_ lpfn
                                                  HINSTANCE,  # _In_ hMod
                                                  DWORD)  # _In_ dwThreadId

        self.user32.CallNextHookEx.restype = LRESULT
        self.user32.CallNextHookEx.argtypes = (HHOOK,  # _In_opt_ hhk
                                               c_int,  # _In_     nCode
                                               WPARAM,  # _In_     wParam
                                               LPARAM)  # _In_     lParam

        self.user32.GetMessageW.argtypes = (LPMSG,  # _Out_    lpMsg
                                            HWND,  # _In_opt_ hWnd
                                            UINT,  # _In_     wMsgFilterMin
                                            UINT)  # _In_     wMsgFilterMax

        self.user32.TranslateMessage.argtypes = (LPMSG,)
        self.user32.DispatchMessageW.argtypes = (LPMSG,)

        @CallWndProc
        def CallbackFunc(nCode, wParam, lParam):
            msg = cast(lParam, LPMSLLHOOKSTRUCT)[0]
            msgid = MSG_TEXT.get(wParam, str(wParam))
            print(nCode, wParam, lParam)
            # print('{:15s}: {}'.format(msgid, msg.wParam))
            if nCode == HC_ACTION:
                if self.WM_WMCA_EVENT == wParam:
                    print("TEST")
                # if wParam == CA_CONNECTED:
                #     print("로그인 성공")
                # elif wParam == CA_DISCONNECTED:
                #     print("접속 끊김")
                # elif wParam == CA_SOCKETERROR:
                #     print("통신 오류 발생")
                # elif wParam == CA_RECEIVEDATA:
                #     print("서비스 응답 수신(TR)")
                # elif wParam == CA_RECEIVESISE:
                #     print("실시간 데이터 수신(BC)")
                # elif wParam == CA_RECEIVEMESSAGE:
                #     print("상태 메시지 수신 (입력값이 잘못되었을 경우 문자열형태로 설명이 수신됨)")
                # elif wParam == CA_RECEIVECOMPLETE:
                #     print("서비스 처리 완료")
                # elif wParam == CA_RECEIVEERROR:
                #     print("서비스 처리중 오류 발생 (입력값 오류등)")
                # elif wParam == self.WM_WMCA_EVENT:
                #     print("EVENT TEST")
                    
            return self.user32.CallNextHookEx(None, nCode, wParam, lParam)

        def wmca_msg_loop():
            hHook = self.user32.SetWindowsHookExW(WH_CALLWNDPROC, CallbackFunc, self.wmca_dll._handle, 0)
            print("hHook : ", hHook)
            msg = MSG()
            while True:
                bRet = self.user32.GetMessageW(byref(msg), None, 0, 0)
                if not bRet:
                    break
                if bRet == -1:
                    raise WinError(get_last_error())
                self.user32.TranslateMessage(byref(msg))
                self.user32.DispatchMessageW(byref(msg))

        t = Thread(target=wmca_msg_loop)
        t.start()
        # while True:
        #     try:
        #         time.sleep(1)
        #     except KeyboardInterrupt:
        #         self.user32.PostThreadMessageW(t.ident, WM_QUIT, 0, 0)
        #         break


flipper_nm = FlipperHelperMynamuh()

root = tk.Tk()

t = Thread(target=flipper_nm.__init__)
t.daemon = True
t.start()

tk.Button(root, text='----------------------------------------------------------------------------').pack()
tk.Button(root, text='SendMessage', command=flipper_nm.SendMessage).pack()
tk.Button(root, text='로그인', command=flipper_nm.wmcaConnect).pack()
tk.Button(root, text='후크', command=flipper_nm.setHook).pack()

root.mainloop()
