# -*- coding: utf-8 -*-
import json
import os
import sys

import win32api
import win32con
import win32gui

from alldev.settings.base import BASE_DIR
from namuh_bot.namuh_structure import *

os.environ['PATH'] = ';'.join([os.environ['PATH'], BASE_DIR + r"\namuh_bot\bin"])

from ctypes.wintypes import *


# Create your tests here.
class NamuhWindow:
    sz_id = ''  # 사용자 아이디
    sz_pw = ''  # 사용자 비밀번호
    sz_cert_pw = ''  # 공인인증서 비밀번호
    account_pw = ''  # 계좌 비밀번호
    trade_pw = ''  # 거래 비밀번호
    is_hts = 'true'  # 모의투자 여부 (True : 모의투자, False : 실투자)
    # callback_class = None
    response = []

    def __init__(self):
        # message map
        message_map = {
            # msg_TaskbarRestart: self.OnRestart,
            # win32con.WM_DESTROY: self.OnDestroy,
            CA_WMCAEVENT: self.wnd_proc,
            CA_RECEIVEERROR: self.wnd_proc,
            # win32con.WM_COMMAND: self.on_command,
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
        print("NamuhWindow START!")

    def create_tray_icons(self):  # 트레이 아이콘 생성
        # Try and find a custom icon
        hinst = win32api.GetModuleHandle(None)
        icon_path_name = os.path.abspath(os.path.join(os.path.split(sys.executable)[0], "pyc.ico"))
        if not os.path.isfile(icon_path_name):
            # Look in DLLs dir, a-la py 2.5
            icon_path_name = os.path.abspath(os.path.join(os.path.split(sys.executable)[0], "DLLs", "pyc.ico"))
        if not os.path.isfile(icon_path_name):
            # Look in the source tree.
            icon_path_name = os.path.abspath(os.path.join(os.path.split(sys.executable)[0], "..\\PC\\pyc.ico"))
        if os.path.isfile(icon_path_name):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(hinst, icon_path_name, win32con.IMAGE_ICON, 0, 0, icon_flags)
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

    def on_command(self, json_data):
        req_id = json_data["req_id"]

        if req_id == "connect":
            print("로그인 시도")
            connect = json_data["param"]
            self.sz_id = connect["sz_id"].encode()
            self.sz_pw = connect["sz_pw"].encode()
            self.sz_cert_pw = connect["sz_cert_pw"].encode()
            self.account_pw = connect["account_pw"].encode()
            self.trade_pw = connect["trade_pw"].encode()
            self.set_is_hts(connect["is_hts"])  # 모의투자 or 실투자 변경

            return self.wmca.connect(self.hwnd, self.sz_id, self.sz_pw, self.sz_cert_pw)

        elif req_id == "query":
            print("일회성 조회")
            query = json_data["param"]

            if self.wmca.is_connected():
                return self.wmca.query(self.hwnd, query["nTRID"], query["szTRCode"], query["szInput"], query["nInputLen"], query["nAccountIndex"])  # nTRID, szTRCode, szInput, nInputLen, nAccountIndex=0
            else:
                print("로그인 되지 않음")  # TODO : 리턴 메시지 작성 필요
                return False

        elif req_id == "attach":
            query = json_data["param"]
            self.wmca.detach_all()
            result = self.wmca.attach(self.hwnd, query["szBCType"], query["szInput"], query["nCodeLen"], query["nInputLen"])  # szBCType, szInput, nCodeLen, nInputLen
            print("실시간 시세 조회 = ", result)
            return result

        elif req_id == "detach_all":
            result = self.wmca.detach_all()
            print("실시간 일괄 취소 = ", result)
            return result

        return 1

    def wnd_proc(self, hwnd, message, wParam, lParam):  # wmca MFC 콜백 처리
        # if wParam == CA_DISCONNECTED:
        #     print("Goodbye")/
        #     win32gui.PostQuitMessage(0)
        #     win32gui.DestroyWindow(self.hwnd)
        # el
        if wParam == CA_CONNECTED:  # 로그인 성공
            print("로그인 성공")
            # self.response.append({"login": "success"})
            win32gui.PostQuitMessage(0)  # mfc 메시지 루프 종료 (메시지를 받고 종료 처리 뒷 프로세스 실행을 위함)
        elif wParam == CA_SOCKETERROR:  # 통신 오류 발생
            print("통신 오류 발생")
        elif wParam == CA_RECEIVEDATA:  # 서비스 응답 수신(TR)
            print("서비스 응답 수신(TR)")
            self.response.append(self.on_wm_receivedata(lParam))
        elif wParam == CA_RECEIVESISE:  # 실시간 데이터 수신(BC)
            print("실시간 데이터 수신(BC)")
            self.response.append(self.on_wm_receivesise(lParam))
        elif wParam == CA_RECEIVEMESSAGE:  # 상태 메시지 수신 (입력값이 잘못되었을 경우 문자열형태로 설명이 수신됨)
            self.response.append(self.on_wm_receivemessage(lParam))
            win32gui.PostQuitMessage(0)
        elif wParam == CA_RECEIVECOMPLETE:  # 서비스 처리 완료
            print("서비스 처리 완료")
            win32gui.PostQuitMessage(0)  # mfc 메시지 루프 종료 (메시지를 받고 종료 처리 뒷 프로세스 실행을 위함)
        elif wParam == CA_RECEIVEERROR:  # 서비스 처리중 오류 발생 (입력값 오류등)
            print("서비스 처리중 오류 발생 (입력값 오류등)")

        return win32gui.DefWindowProc(hwnd, message, wParam, lParam)

    def on_wm_receivemessage(self, lparam):
        try:
            p_msg = OutdatablockStruct.from_address(lparam)
            p_data = ReceivedStruct.from_buffer(p_msg.pData.contents)
            string_buffer = create_string_buffer(p_data.szData[:85], 85)
            msg_header = MsgHeaderStruct.from_buffer(string_buffer)
            msg_cd = msg_header.msg_cd.decode("cp949")
            user_msg = msg_header.user_msg.decode("cp949").strip()
            print("상태 메시지 수신 (입력값이 잘못되었을 경우 문자열형태로 설명이 수신됨) = {1} : {2}".format(p_msg.TrIndex, msg_cd, user_msg))
            return {msg_cd: user_msg}
        except Exception as e:
            print("on_wm_receivemessage Exception = ", e)

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
        python_exe_path = sys.base_exec_prefix  # os.path.dirname(sys.executable)
        # print("python_exe_path :", python_exe_path)
        with open(python_exe_path + '/wmca.ini', 'w', encoding="utf-8") as configfile:  # python.exe 경로에 wmca.ini 생성(해당 경로에서 생성해야 적용됨)
            config.write(configfile, space_around_delimiters=False)  # space_around_delimiters : 환경변수의 공백여부 (공백이 있을 경우 읽지 못함)

        self.wmca.load()

    def request_query(self, param):  # 증권사에 정보 조회
        for node in json.loads(param):
            if self.on_command(node):
                self.response = []
                win32gui.PumpMessages()  # MFC 메시지 수집
        print("success")
        return json.dumps(self.response)

    def on_wm_receivedata(self, lparam):  # OnWmReceivedata( (OUTDATABLOCK*)lParam );
        try:
            p_msg = OutdatablockStruct.from_address(lparam)
            p_data = ReceivedStruct.from_buffer(p_msg.pData.contents)
            n_len = p_data.nLen
            string_buffer = create_string_buffer(p_data.szData[:n_len], n_len)
            sz_block_name = p_data.szBlockName.decode("cp949")

            struct_type = None
            if sz_block_name == 'c1101OutBlock':
                struct_type = (C1101OutBlockStruct * 1)
            elif sz_block_name == 'c1101OutBlock2':
                struct_type = (C1101OutBlock2Struct * (n_len // sizeof(C1101OutBlock2Struct)))
            elif sz_block_name == 'c1101OutBlock3':
                struct_type = (C1101OutBlock3Struct * 1)
            elif sz_block_name == 'c4113OutKospi200':
                struct_type = (C4113OutKospi200Struct * 1)
            elif sz_block_name == 'p1005OutBlock':
                struct_type = (P1005OutBlockStruct * (n_len // sizeof(P1005OutBlockStruct)))
            elif sz_block_name == 'c8102InBlock':
                struct_type = (C8102InBlockStruct * 1)
            elif sz_block_name == 'c8102OutBlock':
                struct_type = (C8102OutBlockStruct * 1)

            sz_data = struct_type.from_buffer(string_buffer)

            # print(f"{p_msg.TrIndex}, {sz_block_name}, {n_len}, {repr(sz_data[:])}")
            # print(repr(sz_data))
            # if sz_block_name == "c1101OutBlock":
            #     print("'" + sz_data.get_str("code") + "'")
            #     print("'" + sz_data.get_str("hname") + "'")

            json_dump = {sz_block_name: [data.get_dict() for data in sz_data]}

            return json_dump
        except Exception as e:
            print("on_wm_receivedata Exception = ", e)

    def on_wm_receivesise(self, lparam):
        try:
            p_msg = OutdatablockStruct.from_address(lparam)
            p_data = ReceivedStruct.from_buffer(p_msg.pData.contents)
            p_sise_data = None
            string_buffer = create_string_buffer(p_data.szData, p_data.nLen)
            if p_data.szBlockName[:2] == b"j8":  # 코스피 주식 현재가(실시간) 수신
                p_sise_data = J8OutBlockStruct.from_buffer(string_buffer, 3)
            elif p_data.szBlockName[:2] == b"d2":  # 실시간 체결통보 => 실시간 체결통보는 별도로 Attach()함수를 호출하지 않아도 자동 수신
                p_sise_data = D2OutBlockStruct.from_buffer(string_buffer, 3)
            elif p_data.szBlockName[:2] == b"d3":  # 실시간 체결통보 => 실시간 체결통보는 별도로 Attach()함수를 호출하지 않아도 자동 수신
                p_sise_data = D3OutBlockStruct.from_buffer(string_buffer, 3)

            print(f"{p_data.szBlockName[:2]} : {repr(p_sise_data)}")
            return p_sise_data
        except Exception as e:
            print("on_wm_receivesise Exception = ", e)

    def encode_hash(self, param):
        json_data = json.loads(param)
        if self.on_command(json_data):
            self.response = []
            win32gui.PumpMessages()  # MFC 메시지 수집

        hash_res = create_string_buffer(44)
        hash_res2 = create_string_buffer(44)
        self.wmca.set_order_pwd(hash_res, json_data['param']['trade_pw'])
        self.response.append({'trade_pw': hash_res.value.decode()})
        self.wmca.set_account_index_pwd(hash_res2, 1, json_data['param']['account_pw'])
        self.response.append({'account_pw': hash_res2.value.decode()})
        return self.response


class WinDllWmca:
    def __init__(self):
        self.wmca_dll = WinDLL('wmca.dll', use_last_error=True)

    def connect(self, hwnd, sz_id, sz_pw, sz_cert_pw):  # 접속 후 로그인(인증)
        func = self.wmca_dll.wmcaConnect
        func.argtypes = [HWND, DWORD, CHAR, CHAR, LPSTR, LPSTR, LPSTR]
        func.restype = BOOL
        result = func(hwnd, CA_WMCAEVENT, b"T", b"W", sz_id, sz_pw, sz_cert_pw)
        # print("connect =", bool(result))
        return bool(result)

    def disconnect(self):  # 접속 해제
        func = self.wmca_dll.wmcaDisconnect
        func.argtypes = []
        func.restype = BOOL
        result = func()
        # print("disconnect =", bool(result))
        return bool(result)

    def is_connected(self):  # 접속 여부 확인
        func = self.wmca_dll.wmcaIsConnected
        func.argtypes = []
        func.restype = BOOL
        result = func()
        # print("is_connected =", bool(result))
        return bool(result)

    def query(self, hwnd, tr_id, sz_tr_code, sz_input, n_input_len, n_account_index=0):  # 서비스(TR) 호출
        func = self.wmca_dll.wmcaQuery
        # HWND hWnd, int nTRID, constchar* szTRCode, const char* szInput, int nInputLen, int nAccountIndex
        func.argtypes = [HWND, INT, LPSTR, LPSTR, INT, INT]
        func.restype = BOOL
        result = func(hwnd, int(tr_id), sz_tr_code.encode(), sz_input.encode(), int(n_input_len), int(n_account_index))
        # print("query =", bool(result))
        return bool(result)

    def attach(self, hwnd, sz_bc_type, sz_input, n_code_len, n_input_len):  # 실시간 등록
        func = self.wmca_dll.wmcaAttach
        # HWND hWnd, const char* szBCType, const char* szInput, int nCodeLen, int nInputLen
        func.argtypes = [HWND, LPSTR, LPSTR, INT, INT]
        func.restype = BOOL
        result = func(hwnd, sz_bc_type.encode(), sz_input.encode(), n_code_len, n_input_len)
        # print("attach =", bool(result))
        return bool(result)

    def detach(self, hwnd, sz_bc_type, sz_input, n_code_len, n_input_len):  # 실시간 취소
        func = self.wmca_dll.wmcaDetach
        # HWND hWnd, const char* szBCType, const char* szInput, int nCodeLen, int nInputLen
        func.argtypes = [HWND, LPSTR, LPSTR, INT, INT]
        func.restype = BOOL
        result = func(hwnd, sz_bc_type.encode(), sz_input.encode(), n_code_len, n_input_len)
        # print("detach =", bool(result))
        return bool(result)

    def detach_window(self, hwnd):  # 실시간 일괄 취소
        func = self.wmca_dll.wmcaDetachWindow
        func.argtypes = [HWND]
        func.restype = BOOL
        result = func(hwnd)
        # print("detach_window =", bool(result))
        return bool(result)

    def detach_all(self):  # 실시간 일괄 취소
        func = self.wmca_dll.wmcaDetachAll
        func.argtypes = []
        func.restype = BOOL
        result = func()
        # print("detach_all =", bool(result))
        return bool(result)

    def load(self):  # dll 실행
        func = self.wmca_dll.wmcaLoad
        func.argtypes = []
        func.restype = BOOL
        result = func()
        # print("load =", bool(result))
        return bool(result)

    def free(self):  # dll 종료
        func = self.wmca_dll.wmcaFree
        func.argtypes = []
        func.restype = BOOL
        result = func()
        # print("free =", bool(result))
        return bool(result)

    def set_order_pwd(self, pass_out, pass_in):  # dll 거래 비밀번호 셋팅
        # func = self.wmca_dll.wmcaSetOrderPwd
        func = self.wmca_dll.wmcaSetOrderPwd
        func.argtypes = [LPSTR, LPSTR]
        func.restype = BOOL
        # result = func(pass_out, pass_in)
        pass_in_buff = create_string_buffer(pass_in.encode(), 8)
        result = func(pass_out, pass_in_buff)

        return bool(result)

    def set_account_index_pwd(self, pass_out, account_index, pass_in):  # dll 계좌 비밀번호 셋팅
        # func = self.wmca_dll.wmcaSetAccountIndexPwd
        # func.argtypes = [c_char_p, INT, c_char_p]
        func = self.wmca_dll.wmcaSetAccountIndexPwd
        func.argtypes = [LPSTR, INT, LPSTR]
        func.restype = BOOL
        # result = func(pass_out, account_index, pass_in)
        pass_in_buff = create_string_buffer(pass_in.encode(), 8)
        result = func(pass_out, account_index, pass_in_buff)

        return bool(result)


if __name__ == '__main__':
    w = NamuhWindow()
