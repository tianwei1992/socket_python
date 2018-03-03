"""
服务器进程首先要绑定一个端口并监听来自其他客户端的连接。如果某个客户端连接过来了，服务器就与该客户端建立Socket连接，随后的通信就靠这个Socket连接了。

"""
import socket
import threading
import time
#这个server是最基础的：它接收客户端连接，把客户端发过来的字符串加上Hello再发回去。

#1创建socket
#其中，参数AF_INET指定使用IPv4协议，如果要用更先进的IPv6，就指定为AF_INET6。SOCK_STREAM指定使用面向流的TCP协议
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

"""
client的第二步是建立连接，server则是绑定ip和端口，然后监听这个连接
"""

#2绑定提供服务的ip+port，并开始listen
#server有多块网卡，可以绑定其中某一块网卡的IP，也可以用0.0.0.0绑定所有，还可以用127.0.0.1绑定到本机地址,如果绑定127.0.0.1，客户端必须同时在本机运行才能连接，也就是说，外部的计算机无法连接进来。
s.bind(('127.0.0.1', 10000))
s.listen(5)
print('Waiting for connection...')

#3监听到客户端连接请求，给与响应

def tcplink(sock, addr):
	#print(sock)#<socket.socket fd=196, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 10000), raddr=('127.0.0.1', 49272)>
	#print(addr)#('127.0.0.1', 49272)
	#这里的响应行为是：1先发送"Welcome!" 2再根据收到的data发送'Hello'+data
	print('Accept new connection from %s:%s...' % addr)#Accept new connection from 127.0.0.1:49239...
	sock.send(b"Welcome!")
	while True:
		data = sock.recv(1024)
		time.sleep(1)
		if not data or data.decode('utf-8') == 'exit':
			break
		#拿到data,先按utf8解码，再修改，修改后按utf8编码编码，再发送
		sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
	sock.close()
	print('Connection from %s:%s closed.' % addr)


while True:
	# （1）accept()会等待并返回一个客户端的连接:
	sock, addr = s.accept()
	# （2）创建新线程来处理TCP连接:
	#创建新线程时，有两个参数target和args，target是响应行为，args是客户端的sock和源信息，也会作为参数传给target
	t = threading.Thread(target=tcplink, args=(sock, addr))
	t.start()
	# （3）定义具体的响应行为,即tcplink的实现


"""
注意到：
字符串都是byte类型而不是str类型，然后实际传输的数据都是经过utf8编码的数据，这意味着发送前要对字符串按utf8编码，接收后第一件事情是按utf8解码
再次，关于编码解码的必要性：换行符经过utf8编码后是\r\n,可以想想如果不经过编码按原始的来，这个换行要怎么传输？所以传输都是经过编码的！当客户端收到\r\n，并不表示服务端表达的是\r\n，可以理解为\r\n类似于密文，绝对不是字面意思。需要经过解码，得到服务端想表达的是换行符！

"""
