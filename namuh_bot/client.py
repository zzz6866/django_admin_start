# -*- coding: utf-8 -*-
import json
import threading
from socket import *

from namuh_bot.socket_message import send_msg


class Client:
    def __init__(self, host, port):
        super().__init__()
        self.client_sock = socket(AF_INET, SOCK_STREAM)
        self.client_sock.connect((host, port))

        print('connect complate !!')

        sender = threading.Thread(target=self.send)
        sender.start()
        receiver = threading.Thread(target=self.receive)
        receiver.start()

    def send(self):
        while True:
            send_data = input('>>>')
            if send_data == "1":
                send_json = json.dumps({"req_id": "login", "is_hts": True, "param": {"sz_id": "start0", "sz_pw": "qpwoei12!", "sz_cert_pw": "ekdnsfhem1!"}})  # sz_id, sz_pw, sz_cert_pw
            elif send_data == "2":
                send_json = json.dumps({"req_id": "query", "param": {"nTRID": 1, "szTRCode": "c1101", "szInput": "K 000120 ", "nInputLen": 8, "nAccountIndex": 0}})  # nTRID, szTRCode, szInput, nInputLen, nAccountIndex=0
            elif send_data == "3":
                send_json = json.dumps({"req_id": "attach", "param": {"szBCType": "h1", "szInput": "005930", "nCodeLen": 6, "nInputLen": 6}})  # nTRID, szTRCode, szInput, nInputLen, nAccountIndex=0
            elif send_data == "4":
                send_json = json.dumps({"req_id": "query", "param": {"nTRID": 1, "szTRCode": "p1005", "szInput": "1", "nInputLen": 1, "nAccountIndex": 0}})  # nTRID, szTRCode, szInput, nInputLen, nAccountIndex=0
            else:
                send_json = ""
            send_msg(self.client_sock, send_json)

    def receive(self):
        while True:
            recv_data = self.client_sock.recv(1024)
            print('chat :', recv_data.decode('utf-8'))


if __name__ == '__main__':
    c = Client(gethostname(), 10003)

# while True:
#     time.sleep(1)
#     pass
