from socket import *

s=socket(AF_INET,SOCK_STREAM)
s.bind(('127.0.0.1',80))
s.listen(5)
#5是backlog的数量，最大建立5个连接，除了当前的其他在后台挂起
print('tcp_server：listening……')

while True:
	#接收一个新的conn，可能该conn已经在后台就等了
	conn,addr=s.accept()
	print('accpet an new connection，with conn={0}。addr={1}'.format(conn,addr))

	while True:
		try:
			data_recv=conn.recv(1024).decode('utf-8')

			data_to_send=(data_recv+'我已经收到了').encode('utf-8')
			f=open("ttttest.html",'rb')


			conn.send(f.read())
			#print('server:message sent,',data_to_send)
		except Exception as e:
			print(e)
			print('exception,go to accpet next ')
			#主要客户端主动断开连接，当前conn不见了，就会异常，这时我们的处理是直接跳出内层while
			#用break而不是continue，表示不是跳出这一轮开始下一轮，而是彻底结束整个循环
			break

	#conn.close()#这一句不执行也没事，因为外层while开头总是会给conn赋新的值，而原有conn看print(conn)还有相关信息，但netstat -an查看已经没有了。大概理解为这个连接已经失效了，但还保持相关信息，但调用会出错。

	print('conn.close被执行')



s.close()
#在于客户端1234全部会话完成后，让s进程关闭，虽然实际应该不是这样……




