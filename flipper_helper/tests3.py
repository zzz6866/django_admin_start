import ctypes
import ctypes.wintypes as wintypes
import tkinter as tk


class CWPRETSTRUCT(ctypes.Structure):
    ''' a class to represent CWPRETSTRUCT structure
    https://msdn.microsoft.com/en-us/library/windows/desktop/ms644963(v=vs.85).aspx '''

    _fields_ = [('lResult', wintypes.LPARAM),
                ('lParam', wintypes.LPARAM),
                ('wParam', wintypes.WPARAM),
                ('message', wintypes.UINT),
                ('hwnd', wintypes.HWND)]


class WINDOWPOS(ctypes.Structure):
    ''' a class to represent WINDOWPOS structure
    https://msdn.microsoft.com/en-gb/library/windows/desktop/ms632612(v=vs.85).aspx '''

    _fields_ = [('hwnd', wintypes.HWND),
                ('hwndInsertAfter', wintypes.HWND),
                ('x', wintypes.INT),
                ('y', wintypes.INT),
                ('cx', wintypes.INT),
                ('cy', wintypes.INT),
                ('flags', wintypes.UINT)]


class App(tk.Tk):
    ''' generic tk app with win api interaction '''

    wm_windowposchanged = 71
    wm_wmca_event = 9424
    wh_callwndprocret = 12
    wh_callwndproc = 4
    wh_getmessage = 3
    swp_noownerzorder = 512
    set_hook = ctypes.windll.user32.SetWindowsHookExW
    call_next_hook = ctypes.windll.user32.CallNextHookEx
    un_hook = ctypes.windll.user32.UnhookWindowsHookEx
    get_thread = ctypes.windll.kernel32.GetCurrentThreadId
    get_error = ctypes.windll.kernel32.GetLastError
    get_parent = ctypes.windll.user32.GetParent
    wnd_ret_proc = ctypes.WINFUNCTYPE(ctypes.c_long, wintypes.INT, wintypes.WPARAM, wintypes.LPARAM)

    def __init__(self):
        ''' generic __init__ '''

        super().__init__()
        self.minsize(700, 400)
        self.hook = self.setup_hook()
        self.protocol('WM_DELETE_WINDOW', self.on_closing)

    def setup_hook(self):
        ''' setting up the hook '''

        thread = self.get_thread()
        # hook = self.set_hook(self.wh_callwndprocret, self.call_wnd_ret_proc, wintypes.HINSTANCE(0), thread)
        # print(hook)
        hook = self.set_hook(self.wh_callwndproc, self.call_wnd_ret_proc, wintypes.HINSTANCE(0), thread)
        print(hook)
        # hook = self.set_hook(self.wh_getmessage, self.call_wnd_ret_proc, wintypes.HINSTANCE(0), thread)
        # print(hook)

        if not hook:
            raise ctypes.WinError(self.get_error())

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
        msg = ctypes.cast(lParam, ctypes.POINTER(CWPRETSTRUCT)).contents
        if msg.message == App.wm_windowposchanged and msg.hwnd == App.get_parent(app.winfo_id()):
            #   if message, which belongs to owner hwnd, is signaling that windows position is changed - check z-order
            wnd_pos = ctypes.cast(msg.lParam, ctypes.POINTER(WINDOWPOS)).contents
            print('z-order changed: %r' % ((wnd_pos.flags & App.swp_noownerzorder) != App.swp_noownerzorder))
        elif msg.message == App.wm_wmca_event and msg.hwnd == App.get_parent(app.winfo_id()):
            print("wm_wmca_event")

        return App.call_next_hook(None, nCode, wParam, lParam)

    def send_message(self):
        result = ctypes.windll.user32.PostMessageW(wintypes.HINSTANCE(0), App.wm_wmca_event, 1, 1)
        result = ctypes.windll.user32.SendMessageW(wintypes.HINSTANCE(0), App.wm_wmca_event, 1, 1)
        result = ctypes.windll.user32.PostMessageW(wintypes.HINSTANCE(0), App.wm_windowposchanged, 1, 1)
        result = ctypes.windll.user32.SendMessageW(wintypes.HINSTANCE(0), App.wm_windowposchanged, 1, 1)


app = App()

tk.Button(app, text='SendMessage', command=app.send_message).pack()

app.mainloop()
