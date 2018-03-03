from socket import *

server_ip_port=('127.0.0.1',9000)
ntp_client=socket(AF_INET,SOCK_DGRAM)
buffer_size=1024
while True:
	user_input=input('>>:').encode('utf-8')
	ntp_client.sendto(user_input,server_ip_port)
	data_recv,ip_port=ntp_client.recvfrom(buffer_size)
	print(data_recv.decode('utf-8'))


ntp_client.close()
