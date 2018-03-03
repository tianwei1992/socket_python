"""
使用UDP协议时，不需要建立连接，只需要知道对方的IP地址和端口号，就可以直接发数据包。但是，能不能到达就不知道了。
"""
import socket

# 1创建socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 其中，SOCK_DGRAM指定了这个Socket的类型是UDP。

# 2绑定提供服务的ip+port，但不需要listen，直接接收首客户端数据就是
s.bind(('127.0.0.1', 9999))
print('Bind UDP on 9999...')

# 3 开始接收客户端
"""
没有tcp中为每一个客户端创建新线程，然后在新线程中响应的这个步骤，而是直接s.sendto响应，对所有客户端都在主程序中一并处理

	sock, addr = s.accept()
	t = threading.Thread(target=tcplink, args=(sock, addr))
	t.start()
"""
while True:
	# 接收数据:
	data, addr = s.recvfrom(1024)
	print('Received from %s:%s.' % addr)
	s.sendto(b'Hello, %s!' % data, addr)
	# recvfrom()方法返回data和源addr，这样，服务器收到数据后，可以对data进行处理，然后调用sendto()把处理后的data用UDP发给客户端。
