from socket import *
udp_client=socket(AF_INET,SOCK_DGRAM)

server_ip_port=('127.0.0.1',9000)
buffer_size=1024

while True:
	data_input=input('>:').strip()
	udp_client.sendto(data_input.encode('utf-8'),server_ip_port)
	data,from_ip_port=udp_client.recvfrom(buffer_size)
	print(data.decode('utf-8'))

udp_client.close()

