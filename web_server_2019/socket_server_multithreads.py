import threading
import errno
import time
import socket
import platform


from socket_server import EOL1, EOL2, body


body += 'from {thread_name}'
response_params = [
    'HTTP/1.0 200 0K',
    'Date: Sun, 05 March 2019 21:22:01 GMT',
    # 'Content-Type: text/plain; charset=utf-8',
    'Content-Type: text/html; charset=utf-8',
    'Content-Length: {length}\r\n',
    body,
]
response = '\r\n'.join(response_params)


def handle_connection(conn, addr):
    request = b''
    while EOL1 not in request and EOL2 not in request:
        request += conn.recv(1024)

    print(request)

    current_thread = threading.currentThread()
    print(current_thread.name)
    content_length = len(body.format(thread_name=current_thread.name).encode('utf-8'))

    conn.send(response.format(thread_name=current_thread.name, length=content_length).encode('utf-8'))
    conn.close()


def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.setblocking(1) # 非阻塞，accpet()和recv()两行，没有收到对方时会往下，不会卡住，
    serversocket.bind(('127.0.0.1', 8000))
    serversocket.listen(10)
    print("READY!")
    EXCP_TO_IGNORE = errno.EWOULDBLOCK if platform.system().startswith("Windows")else errno.EAGAIN


    try:
        i = 0
        while True:
            try:
                conn, address = serversocket.accept()
            except socket.error as e:
                if e.args[0] != EXCP_TO_IGNORE:
                    # 非阻塞下，accpet()没有拿到连接时，会报EAGAIN的错误，其实是正常的，算异常
                    raise    # 是意料外的错误，需要报出来
                continue    # 否则是预料的异常，不管，继续
            i = i + 1
            print(i)
            t = threading.Thread(target=handle_connection, args=(conn, address), name='thread-%s'%i)
            t.start()
    finally:
        serversocket.close()


if __name__ == "__main__":
    main()

