import socket

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'
body = '''Hello,world! <h1>我在学习Django呢~</h1>'''
response_params = [
    'HTTP/1.0 200 0K',
    'Date: Sun, 05 March 2019 21:22:01 GMT',
    # 'Content-Type: text/plain; charset=utf-8',
    'Content-Type: text/html; charset=utf-8',
    'Content-Length: {}\r\n'.format(len(body.encode())),
    body,
]
response = '\r\n'.join(response_params)


def handle_connect(conn, addr):
    # receive part by part, and then concact to a complete request
    print("new conn:{},{}".format(conn, addr))

    import time
    # time.sleep(50) #模拟任务处理时间

    request = b""
    while EOL1 not in request and EOL2 not in request:
        request += conn.recv(1024)
    print(request)

    # in this case ,the response is fixed whatever the request is
    conn.send(response.encode('utf-8'))

    conn.close()


def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)     # 设置套接字可复用
    serversocket.bind(('127.0.0.1', 9999))
    serversocket.listen(5)    # set backlog
    print("Ready!")

    try:
        while True:
            conn, address = serversocket.accept()
            handle_connect(conn, address)
    finally:
        serversocket.close()


if __name__ == "__main__":
    main()