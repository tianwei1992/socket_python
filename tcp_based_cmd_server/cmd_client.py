from socket import *


ip_port=('127.0.0.1',8080)
buffer_size=64

cmd_client=socket(AF_INET,SOCK_STREAM)
cmd_client.connect(ip_port)

while True:
	print("提示：输入exit退出")
	cmd=input('>>:').strip()

	#特殊情况1：输入空
	if not cmd:
		continue
	#特殊情况2：输入exit
	elif cmd=='exit':
		break
	else:
		cmd_client.send(cmd.encode('utf-8'))
	#以上发送完毕，以下开始接收……
	cmd_res=cmd_client.recv(buffer_size)
	#注意对方不是按utf8编码的……
	#print(cmd_res)
	print(cmd_res.decode('GB2312'))

cmd_client.close()