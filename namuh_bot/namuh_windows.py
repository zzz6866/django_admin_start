import json
import os
import socket
import sys
import threading

import win32api
import win32con
import win32gui

from alldev.settings.base import BASE_DIR
from namuh_bot.models import *

# from celery.utils.log import get_task_logger
# logger = get_task_logger(__name__)

os.environ['PATH'] = ';'.join([os.environ['PATH'], BASE_DIR + r"\namuh_bot\bin"])

from ctypes.wintypes import *

'''
import socket
import json

# 서버 호스트 : 클라이언트가 접속할 IP
HOST = socket.gethostname()

# 서버포트 : 클라이언트가 접속할 포트
PORT = 10003

# 소켓 객체 생성
# socket.AF_INET : IPv4 체계 사용
# socket.SOCK_STREAM : TCP 소켓 타입 사용
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))
# HOST와 PORT로 서버 연결 시도
cmd = "query"
send_json = None
if cmd == "login":
    send_json = json.dumps({"req_id": "login", "param": {"sz_id": "start0", "sz_pw": "qpwoei12!", "sz_cert_pw": "ekdnsfhem1!"}})  # sz_id, sz_pw, sz_cert_pw
elif cmd == "query":
    send_json = json.dumps({"req_id": "query", "param": {"nTRID": 1, "szTRCode": "c1101", "szInput": "K 217620 ", "nInputLen": 9, "nAccountIndex": 0}})  # nTRID, szTRCode, szInput, nInputLen, nAccountIndex=0
elif cmd == "attach":
    send_json = json.dumps({"req_id": "attach", "param": {"szBCType": "h1", "szInput": "005940", "nCodeLen": 217620, "nInputLen": 6}})  # nTRID, szTRCode, szInput, nInputLen, nAccountIndex=0

if send_json:
    # 메시지 전송
    client_socket.sendall(send_json.encode())

    # 메시지 수신
    data = client_socket.recv(1024)
    print('Received : ', repr(data.decode()))
# 소켓 close
client_socket.close()

'''


# Create your tests here.
class NamuhWindow:
    sz_id = ""  # 사용자 아이디
    sz_pw = ""  # 사용자 비밀번호
    sz_cert_pw = ""  # 공인인증서 비밀번호
    is_while = False  # 가격 체크를 위한 루프 변수 (True : 실시간 체크, False : 루프 종료)
    is_hts = True  # 모의투자 여부 (True : 모의투자, False : 실투자)

    def __init__(self):
        # message map
        message_map = {
            # msg_TaskbarRestart: self.OnRestart,
            # win32con.WM_DESTROY: self.OnDestroy,
            CA_WMCAEVENT: self.wnd_proc,
            CA_RECEIVEERROR: self.wnd_proc,
            win32con.WM_COMMAND: self.on_command,
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
        self.hwnd = win32gui.CreateWindow(wc.lpszClassName,
                                          "Namuh Window",
                                          wc.style,
                                          0,
                                          0,
                                          win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT,
                                          0,
                                          0,
                                          wc.hInstance,
                                          None)

        # Show Window
        # win32gui.ShowWindow(self.hwnd, SW_SHOWNORMAL)
        win32gui.UpdateWindow(self.hwnd)

        self.create_tray_icons()  # 트레이 아이콘 생성

        self.wmca = WinDllWmca()  # 모바일증권 나무 DLL 로드
        t = threading.Thread(target=self.recive_message)
        t.daemon = True
        t.start()
        print(self.__class__, " START!")

    def create_tray_icons(self):  # 트레이 아이콘 생성
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

    def on_command(self, hwnd, message, wParam, lParam):
        # req = cast(wParam, c_char_p).value.decode('utf-8')
        param = json.loads(cast(lParam, c_char_p).value.decode('utf-8'))
        req_id = param["req_id"]
        if message == win32con.WM_DESTROY or wParam == MENU_EXIT:  # 윈도우 창 닫기 버튼 클릭시 # 접속 끊김
            print("Goodbye")
            win32gui.PostQuitMessage(0)
            win32gui.DestroyWindow(self.hwnd)

        elif req_id == "login":
            print("로그인 시도")
            login = param["param"]
            self.sz_id = login["sz_id"].encode()
            self.sz_pw = login["sz_pw"].encode()
            self.sz_cert_pw = login["sz_cert_pw"].encode()

            self.set_is_hts(param["is_hts"])  # 모의투자 or 실투자 변경

            self.wmca.connect(self.hwnd, self.sz_id, self.sz_pw, self.sz_cert_pw)

        elif req_id == "query":
            print("시세 조회")
            query = param["param"]

            if self.wmca.is_connected():
                self.wmca.query(self.hwnd, query["nTRID"], query["szTRCode"], query["szInput"], query["nInputLen"], query["nAccountIndex"])  # nTRID, szTRCode, szInput, nInputLen, nAccountIndex=0
            else:
                print("로그인 되지 않음")  # TODO : 리턴 메시지 작성 필요

        elif req_id == "attach":
            print("실시간 시세 조회")
            query = param["param"]
            self.wmca.attach(self.hwnd, query["szBCType"], query["szInput"], query["nCodeLen"], query["nInputLen"])  # szBCType, szInput, nCodeLen, nInputLen

        return win32gui.DefWindowProc(hwnd, message, wParam, lParam)

    def wnd_proc(self, hwnd, message, wParam, lParam):  # wmca MFC 콜백 처리
        # if wParam == CA_DISCONNECTED:
        #     print("Goodbye")
        #     win32gui.PostQuitMessage(0)
        #     win32gui.DestroyWindow(self.hwnd)
        # el
        if wParam == CA_CONNECTED:  # 로그인 성공
            print("로그인 성공")
        elif wParam == CA_SOCKETERROR:  # 통신 오류 발생
            print("통신 오류 발생")
        elif wParam == CA_RECEIVEDATA:  # 서비스 응답 수신(TR)
            print("서비스 응답 수신(TR)")
            self.on_wm_receivedata(lParam)
        elif wParam == CA_RECEIVESISE:  # 실시간 데이터 수신(BC)
            print("실시간 데이터 수신(BC)")
        elif wParam == CA_RECEIVEMESSAGE:  # 상태 메시지 수신 (입력값이 잘못되었을 경우 문자열형태로 설명이 수신됨)
            self.on_wm_receivemessage(lParam)
        elif wParam == CA_RECEIVECOMPLETE:  # 서비스 처리 완료
            print("서비스 처리 완료")
        elif wParam == CA_RECEIVEERROR:  # 서비스 처리중 오류 발생 (입력값 오류등)
            print("서비스 처리중 오류 발생 (입력값 오류등)")
        return win32gui.DefWindowProc(hwnd, message, wParam, lParam)

    def on_wm_receivemessage(self, lParam):
        try:
            p_msg = cast(lParam, POINTER(OutdatablockStruct))
            p_msg_header = cast(p_msg.contents.pData.contents.szData, POINTER(MsgHeaderStruct))
            msg_cd = p_msg_header.contents.msg_cd.decode("utf-8")
            user_msg = p_msg_header.contents.user_msg.decode("euc-kr")
            print("상태 메시지 수신 (입력값이 잘못되었을 경우 문자열형태로 설명이 수신됨) = {1} : {2}".format(p_msg.contents.TrIndex, msg_cd, user_msg))
        except UnicodeDecodeError as e:
            print("UnicodeDecodeError = ", e)

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
            win32gui.AppendMenu(menu, win32con.MF_STRING, 1000, "LOGIN")
            win32gui.AppendMenu(menu, win32con.MF_STRING, MENU_EXIT, "Exit program")
            pos = win32gui.GetCursorPos()
            # See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winui/menus_0hdi.asp
            win32gui.SetForegroundWindow(self.hwnd)
            win32gui.TrackPopupMenu(menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, self.hwnd, None)
            win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)
        return 1

    def set_is_hts(self, is_hts):
        self.is_hts = is_hts

        if is_hts:  # 모의투자일 경우
            wmca_server = "newmt.wontrading.com"
            wmca_port = "8400"
        else:  # 실투자일 경우
            wmca_server = "wmca.nhqv.com"
            wmca_port = "8200"

        import configparser
        import os
        import sys

        config = configparser.ConfigParser()
        config.set("", "server", wmca_server)
        config.set("", "port", wmca_port)
        config.set("", "로그사용", "Y")
        python_exe_path = os.path.dirname(sys.executable)
        # print(python_exe_path)
        with open(python_exe_path + '/wmca.ini', 'w') as configfile:  # python.exe 경로에 wmca.ini 생성(해당 경로에서 생성해야 적용됨)
            config.write(configfile, space_around_delimiters=False)  # space_around_delimiters : 환경변수의 공백여부 (공백이 있을 경우 읽지 못함)

        self.wmca.load()

    def recive_message(self):
        # 서버 호스트 : 클라이언트가 접속할 IP
        sockert_host = socket.gethostname()

        # 서버포트 : 클라이언트가 접속할 포트
        sockert_port = 10003

        # 소켓 객체 생성
        # socket.AF_INET : IPv4 체계 사용
        # socket.SOCK_STREAM : TCP 소켓 타입 사용
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # WinError 10048 에러 방지를 위한 환경 선언( 포트 사용중 방지 )
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 인터페이스
        server_socket.bind((sockert_host, sockert_port))

        # 서버 포트 허용
        server_socket.listen()

        try:
            # 메시지 무제한 수신을 위한 무한루프
            while True:
                # 통신 대기 및 클라이언트 소켓 리턴
                client_socket, addr = server_socket.accept()
                print('Connected by', addr)

                # 메시지 버퍼 크기 지정
                data = client_socket.recv(1024)

                # 메시지 출력
                print('Received from', addr, json.loads(data.decode()))

                self.request_query(data)

                # 받은 메시지 재전송(메시지 반환)
                client_socket.sendall(data)
                # 소켓 close
                client_socket.close()
        except Exception as error:
            print("socket recived message error : ", error)
        finally:
            # 소켓 close
            server_socket.close()

    def request_query(self, param):  # 증권사에 정보 조회
        win32gui.PostMessage(self.hwnd, win32con.WM_COMMAND, 0, param)
        # BOOL    wmcaQuery(HWND hWnd, int nTRID, const char* szTRCode, const char* szInput, int nInputLen, int nAccountIndex=0);
        # self.wmca.query(self.hwnd, 0, b"c1101", b"K000000", 7, 0)

    def on_wm_receivedata(self, lParam):  # OnWmReceivedata( (OUTDATABLOCK*)lParam );
        try:
            p_msg = cast(lParam, POINTER(OutdatablockStruct))
            p_msg_header = cast(p_msg.contents.pData, POINTER(ReceivedStruct))
            szBlockName = p_msg_header.contents.szBlockName.decode()

            struct_type = None
            if szBlockName == "c1101OutBlock":
                struct_type = POINTER(c1101OutBlockStruct)
            elif szBlockName == "c1101OutBlock2":
                struct_type = POINTER(c1101OutBlock2Struct)
            elif szBlockName == "c1101OutBlock3":
                struct_type = POINTER(c1101OutBlock3Struct)
            szData = cast(p_msg_header.contents.szData, struct_type)
            nLen = p_msg_header.contents.nLen

            print(f"{p_msg.contents.TrIndex}, {szBlockName}, {szData.contents}, {nLen}")
        except Exception as e:
            print("Exception = ", e)


class WinDllWmca:
    def __init__(self):
        self.wmca_dll = windll.LoadLibrary('wmca.dll')

    def connect(self, hwnd, sz_id, sz_pw, sz_cert_pw):  # 접속 후 로그인(인증)
        func = self.wmca_dll.wmcaConnect
        func.argtypes = [HWND, DWORD, CHAR, CHAR, LPSTR, LPSTR, LPSTR]
        func.restype = BOOL
        result = func(hwnd, CA_WMCAEVENT, b"T", b"W", sz_id, sz_pw, sz_cert_pw)
        # print("connect =", bool(result))

    def disconnect(self):  # 접속 해제
        func = self.wmca_dll.wmcaDisconnect
        func.argtypes = []
        func.restype = BOOL
        result = func()
        # print("disconnect =", bool(result))

    def is_connected(self):  # 접속 여부 확인
        func = self.wmca_dll.wmcaIsConnected
        func.argtypes = []
        func.restype = BOOL
        result = func()
        # print("is_connected =", bool(result))
        return bool(result)

    def query(self, hwnd, nTRID, szTRCode, szInput, nInputLen, nAccountIndex=0):  # 서비스(TR) 호출
        func = self.wmca_dll.wmcaQuery
        # HWND hWnd, int nTRID, constchar* szTRCode, const char* szInput, int nInputLen, int nAccountIndex
        func.argtypes = [HWND, INT, LPSTR, LPSTR, INT, INT]
        func.restype = BOOL
        result = func(hwnd, nTRID, szTRCode.encode(), szInput.encode(), nInputLen, nAccountIndex)
        # print("query =", bool(result))

    def attach(self, hwnd, szBCType, szInput, nCodeLen, nInputLen):  # 실시간 등록
        func = self.wmca_dll.wmcaAttach
        # HWND hWnd, const char* szBCType, const char* szInput, int nCodeLen, int nInputLen
        func.argtypes = [HWND, LPSTR, LPSTR, INT, INT]
        func.restype = BOOL
        result = func(hwnd, szBCType.encode(), szInput.encode(), nCodeLen, nInputLen)
        # print("attach =", bool(result))

    def detach(self, hwnd, szBCType, szInput, nCodeLen, nInputLen):  # 실시간 취소
        func = self.wmca_dll.wmcaDetach
        # HWND hWnd, const char* szBCType, const char* szInput, int nCodeLen, int nInputLen
        func.argtypes = [HWND, LPSTR, LPSTR, INT, INT]
        func.restype = BOOL
        result = func(hwnd, szBCType.encode(), szInput.encode(), nCodeLen, nInputLen)
        # print("detach =", bool(result))

    def detach_window(self, hwnd):  # 실시간 일괄 취소
        func = self.wmca_dll.wmcaDetachWindow
        func.argtypes = [HWND]
        func.restype = BOOL
        result = func(hwnd)
        # print("detach_window =", bool(result))

    def detach_all(self):  # 실시간 일괄 취소
        func = self.wmca_dll.wmcaDetachAll
        func.argtypes = []
        func.restype = BOOL
        result = func()
        # print("detach_all =", bool(result))

    def load(self):  # dll 실행
        func = self.wmca_dll.wmcaLoad
        func.argtypes = []
        func.restype = BOOL
        result = func()
        # print("load =", bool(result))

    def free(self):  # dll 종료
        func = self.wmca_dll.wmcaFree
        func.argtypes = []
        func.restype = BOOL
        result = func()
        # print("free =", bool(result))


if __name__ == '__main__':
    w = NamuhWindow()
    win32gui.PumpMessages()  # MFC 메시지 수집
