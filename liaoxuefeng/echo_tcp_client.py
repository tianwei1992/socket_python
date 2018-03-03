#配合echo_server.py，这个文件模拟客户端

import socket



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#1 建立连接:
s.connect(('127.0.0.1', 10000))

# 2收发消息:
print(s.recv(1024).decode('utf-8'))
for data in [b'Michael', b'Tracy', b'Sarah']:
	# 发送数据:
	s.send(data)
	#收到后按utf8解码
	print(s.recv(1024).decode('utf-8'))
s.send(b'exit')
s.close()