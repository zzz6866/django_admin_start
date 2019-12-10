import sys
import time
import ctypes
import ctypes.wintypes
import win32api
import win32con
import win32gui
from pywinauto.win32_hooks import Hook
from pywinauto.win32_hooks import MouseEvent

WINEVENT_OUTOFCONTEXT = 0x0000
EVENT_SYSTEM_MENUSTART = 0x0004
EVENT_SYSTEM_MENUEND = 0x0005

SYSMENU_WIDTH = 200
SYSMENU_HEIGHT = 300

user32 = ctypes.windll.user32
ole32 = ctypes.windll.ole32
ole32.CoInitialize(0)

# Текущее соостояние слежения
state = 0

# Текущие координаты окна
base_x = 0
base_y = 0


def on_click(args):
    global state
    if isinstance(args, MouseEvent):
        if args.current_key == 'LButton' and args.event_type == 'key down':
            if state == 0:
                state = 1
            elif state == 2 and (args.mouse_x < base_x+SYSMENU_WIDTH and
                                 args.mouse_y < base_y+SYSMENU_HEIGHT):
                print('That is! Command from system menu!')
                state = 3
            else:
                state = 0


def on_menu_show(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
    # idObject - тип вызванного меню
    global state
    global base_x
    global base_y
    rect = win32gui.GetWindowRect(hwnd)
    base_x = rect[0]
    base_y = rect[1]
    if idObject == -1:
        state = 2


def on_menu_close(hWinEventHook, event, hwnd, idObject, idChild, dwEventThread, dwmsEventTime):
    global state
    if idObject == -1:
        if state == 3:
            state = 0

def main():

    # Исходный код добавления нового пункта меню
    hwnd = win32gui.GetForegroundWindow()
    hmenu = win32gui.GetSystemMenu(hwnd, False)
    win32gui.AppendMenu(hmenu, win32con.MF_STRING, 1248, 'Test')

    # Установка хуков на показ/скрытие объекта "Меню"
    WinEventProcType = ctypes.WINFUNCTYPE(
        None,
        ctypes.wintypes.HANDLE,
        ctypes.wintypes.DWORD,
        ctypes.wintypes.HWND,
        ctypes.wintypes.LONG,
        ctypes.wintypes.LONG,
        ctypes.wintypes.DWORD,
        ctypes.wintypes.DWORD
    )

    WinEventProc1 = WinEventProcType(on_menu_show)
    WinEventProc2 = WinEventProcType(on_menu_close)

    user32.SetWinEventHook.restype = ctypes.wintypes.HANDLE
    hook1 = user32.SetWinEventHook(
        EVENT_SYSTEM_MENUSTART,
        EVENT_SYSTEM_MENUSTART,
        0,
        WinEventProc1,
        0,
        0,
        WINEVENT_OUTOFCONTEXT
    )

    if hook1 == 0:
        print('SetWinEventHook failed')
        sys.exit(1)

    hook2 = user32.SetWinEventHook(
        EVENT_SYSTEM_MENUEND,
        EVENT_SYSTEM_MENUEND,
        0,
        WinEventProc2,
        0,
        0,
        WINEVENT_OUTOFCONTEXT
    )

    if hook2 == 0:
        print('SetWinEventHook failed')
        sys.exit(1)

    # Установка хука на клик мыши
    hook3 = Hook()
    hook3.handler = on_click
    hook3.hook(keyboard=False, mouse=True)

    # Обработка сообщений показа/скрытия меню.
    msg = ctypes.wintypes.MSG()
    while user32.GetMessageW(ctypes.byref(msg), 0, 0, 0) != 0:
        user32.TranslateMessageW(msg)
        user32.DispatchMessageW(msg)

    user32.UnhookWinEvent(hook1)
    user32.UnhookWinEvent(hook2)
    user32.UnhookWinEvent(hook3)
    ole32.CoUninitialize()


if __name__ == '__main__':
    main()