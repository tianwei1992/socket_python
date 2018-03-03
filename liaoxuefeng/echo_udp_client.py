import socket

#1 创建socket
# 其中，SOCK_DGRAM指定了这个Socket的类型是UDP。
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#2 收发消息
for data in [b'Michael', b'Tracy', b'Sarah']:
    # 发送数据:
    s.sendto(data, ('127.0.0.1', 9999))
    # 接收数据:
    print(s.recv(1024).decode('utf-8'))
s.close()

"""

注意：
（1）UDP客户端，发送时用s.sendto方法，参数有两个，data和addr
而TCP客户端，发送用s.send方法，参数只有一个，data，这是因为TCP 的socket在收发数据前有个建立连接的过程s.connect(('127.0.0.1', 10000))，这里通信双方已经确认好了addr。

（2）无论TCP还是UDP客户端，接收是都用s.recv()方法，这个是没有区别的
（3）服务器绑定UDP端口和TCP端口互不冲突，也就是说，服务器上UDP的9999端口与TCP的9999端口可以同时存在


"""