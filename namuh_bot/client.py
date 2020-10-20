# -*- coding: utf-8 -*-
import socket
import json

# 테스트용 소켓 클라이언트 (종료시까지 대화형으로 가능)

# 서버 호스트 : 클라이언트가 접속할 IP
HOST = "192.168.0.2"

# 서버포트 : 클라이언트가 접속할 포트
PORT = 10003

# 소켓 객체 생성
# socket.AF_INET : IPv4 체계 사용
# socket.SOCK_STREAM : TCP 소켓 타입 사용
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))
# HOST와 PORT로 서버 연결 시도
try:
    while True:
        cmd = input(">>>>")
        send_json = None
        if cmd == "1":
            send_json = json.dumps({"req_id": "login", "param": {"is_hts": True, "sz_id": "start0", "sz_pw": "qpwoei12!", "sz_cert_pw": "ekdnsfhem1!"}})  # sz_id, sz_pw, sz_cert_pw
        elif cmd == "2":
            send_json = json.dumps({"req_id": "query", "param": {"nTRID": 1, "szTRCode": "c1101", "szInput": "K 000120 ", "nInputLen": 8, "nAccountIndex": 0}})  # nTRID, szTRCode, szInput, nInputLen, nAccountIndex=0
        elif cmd == "3":
            send_json = json.dumps({"req_id": "attach", "param": {"szBCType": "h1", "szInput": "005930", "nCodeLen": 6, "nInputLen": 6}})  # nTRID, szTRCode, szInput, nInputLen, nAccountIndex=0
        elif cmd == "4":
            send_json = json.dumps({"req_id": "query", "param": {"nTRID": 1, "szTRCode": "p1005", "szInput": "1", "nInputLen": 1, "nAccountIndex": 0}})  # nTRID, szTRCode, szInput, nInputLen, nAccountIndex=0
        else:
            send_json = ""

        if len(send_json) == 0:
            break
        else:
            # 메시지 전송
            client_socket.sendall(send_json.encode())

            # 메시지 수신
            data = client_socket.recv(1024)
            print('Received : ', repr(data.decode()))
except Exception as e:
    print(e)
finally:
    # 소켓 close
    client_socket.close()
