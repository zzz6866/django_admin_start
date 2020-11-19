import http.server
from urllib.parse import urlparse

from namuh_bot.namuh_windows import NamuhWindow


# HTTP Request class
class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):  # simple http web server
    namuh = NamuhWindow()
    timeout = 6  # 타임아웃 5초

    def do_GET(self):  # HTTP request GET
        self.request_get_mapping()

    def do_POST(self):  # HTTP request POST
        # print(f'timeout is {self.timeout} seconds')
        self.request_post_mapping()

    def request_get_mapping(self):  # get path mapping
        request_map = urlparse(self.path)
        if request_map.path == '/hello':
            self.hello()
        else:
            self.reponse_404_not_found()

    def request_post_mapping(self):  # post path mapping
        request_map = urlparse(self.path)
        if request_map.path == '/namuh_windows':
            self.namuh_windows(request_map.query)
        else:
            self.reponse_404_not_found()

    def hello(self):  #
        # HTTP status 200
        self.response(200, 'hello : test')

    def namuh_windows(self, query):  #
        content_len = int(self.headers.get('content-length', 0))
        body = self.rfile.read(content_len).decode('utf-8')
        # HTTP response status 200
        res = self.namuh.request_query(body)
        self.response(200, res)

    def reponse_404_not_found(self):  # HTTP status 404  : not found
        self.response(404, '404 Not Found')

    def response(self, status_code, body):  # HTTP Response send
        # send status
        self.send_response(status_code)

        # send header
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()

        # send body
        self.wfile.write(str(body).encode('utf-8'))


if __name__ == '__main__':
    # request address, port
    ADDRESS = ('localhost', 10003)
    # wait request
    listener = http.server.HTTPServer(ADDRESS, SimpleHTTPRequestHandler)  #
    print(f'http://{ADDRESS[0]}:{ADDRESS[1]} wait request connect...')

    listener.serve_forever()
    # t = threading.Thread(target=listener.serve_forever)
    # t.daemon = True
    # t.start()
    # win32gui.PumpMessages()  # MFC 메시지 수집
