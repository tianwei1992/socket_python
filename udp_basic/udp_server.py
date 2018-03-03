from socket import *


ip_port=('127.0.0.1',9000)
udp_server=socket(AF_INET,SOCK_DGRAM)
udp_server.bind(ip_port)

buffer_size=1024
while True:
	data_recv,from_ip_port=udp_server.recvfrom(buffer_size)
	data_to_send=data_recv.decode('utf-8').upper().encode('utf-8')
	print(data_to_send)
	udp_server.sendto(data_to_send,from_ip_port)

udp_server.close()
