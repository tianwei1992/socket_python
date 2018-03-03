from socket import *

s=socket(AF_INET,SOCK_STREAM)
s.connect(('127.0.0.1',8002))

while True:
	print('提示：输入exit关闭本进程')
	data_to_send=input('>>;').strip()
	if not data_to_send:
		continue
	if data_to_send == 'exit':
		break
	s.send(data_to_send.encode('utf-8'))
	data_recv=s.recv(1024).decode('utf-8')
	print('clent2 recv:',data_recv)


s.close()