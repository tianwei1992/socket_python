
import socket

# 1创建一个socket:
#其中，参数AF_INET指定使用IPv4协议，如果要用更先进的IPv6，就指定为AF_INET6。SOCK_STREAM指定使用面向流的TCP协议
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2建立连接:
s.connect(('www.sina.com.cn', 80))

# 3发送数据:
s.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')

# 4接收数据:
buffer = []
while True:
	# 1024表示每次最多接收1024Byte:
	d = s.recv(1024)
	#print(type(d))<class 'bytes'>
	if d:
		buffer.append(d)
	else:
		#d为空，即s.recv()返回空数据，表示接收完毕，退出循环。
		break
#把buffer列表中的元素join成字符串，因为d是<class 'bytes'>，因此这里data也是bytes类型
data=b''.join(buffer)
# 5关闭连接:
s.close()

#6保存与显示
#分离headers与html
header, html = data.split(b'\r\n\r\n', 1)
#print(header)
#换行经过utf8编码变成了\r\n
#header后跟.decode('utf-8')，\r\n经过解码成为换行
print(header.decode('utf-8'))
# 把接收的数据写入文件:
#因为html是bytes类型，就用'wb'打开；是str类型，就用'w'打开
with open('sina.html', 'wb') as f:
	f.write(html)


"""
需要注意的是，str还是bytes的问题。这里d = s.recv(1024)，拿到的d是bytes类型，所以join成data，data也是bytes类型，最后write to file时，file也要以'wb'方式打开

"""