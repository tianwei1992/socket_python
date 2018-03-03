from socket import *
import time

my_ip_port=('127.0.0.1',9000)
buffer_size=1024

ntp_server=socket(AF_INET,SOCK_DGRAM)
ntp_server.bind(my_ip_port)

while True:
	data,client_ip_port=ntp_server.recvfrom(buffer_size)
	if not data:
		fmt='%Y-%m-%d %H:%M'
	else:
		fmt=data.decode('utf-8')
	print(fmt)
	try:
		ntp_server.sendto(('ntp_server为你报时:'+time.strftime(fmt)).encode('utf-8'),client_ip_port)
	except:
		ntp_server.sendto('输入格式错误'.encode('utf-8'),client_ip_port)

ntp_server.close()