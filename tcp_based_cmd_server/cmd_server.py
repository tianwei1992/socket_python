from socket import *
import subprocess

ip_port=('127.0.0.1',8080)
buffer_size=1024
back_log=5

cmd_server=socket(AF_INET,SOCK_STREAM)
cmd_server.bind(ip_port)
cmd_server.listen(back_log)


def exe_cmd(cmd):
	res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	print('res=',res)
	cmd_res = res.stdout.read()
	return cmd_res

while True:
	print('New Connection--------------')
	conn,client_ip_port=cmd_server.accept()
	print('取到一个新的会话',conn)

	while True:
		try:
			#1接收
			cmd=conn.recv(buffer_size).decode('utf-8')
			print('cmd=',cmd)
			#2以下是处理cmd_recv，生成cmd_res
			cmd_res=exe_cmd(cmd)
			print('cmd_res=',cmd_res)
			#type(cmd_res)已经是bytes，所以不需要编码直接发送，但这个编码的工作是由read()完成的，所以编码方式默认是操作系统的gbk
			#注意这里的编码问题
			if not cmd_res:
				cmd_res='输入无结果，请重新输入'.encode('GB2312')
			#3发送
			print('before send,conn=',conn)
			conn.send(cmd_res)
			print('SEND DONE')
		except Exception as e:
			#在windows上，如果client主动断开了连接，conn就不在了，表现为发生异常，利用这个特点，在服务端检测到异常就break，不拖累服务端一直等待
			print(e)
			break


cmd_server.close()