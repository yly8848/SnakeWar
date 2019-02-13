#/TCP/TCP_Client
#_*_coding:utf-8_*_

import threading
import socket

class TCP_Server(threading.Thread):
	"""TCP服务端工具类"""

	def __init__(self, address,function):
		"""
		Args:
			address: 用于绑定TPC的地址和端口的元组
			function: 接口函数,用于接收和处理客户端的连接

		"""

		super(TCP_Server, self).__init__()

		self.address = address
		self.function=function

		self.serverTCP=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.serverTCP.bind(self.address)
		self.serverTCP.listen(5)

		self.start()

	def run(self):
		while True:
			clientsock,clientaddr=self.serverTCP.accept()
			self.function(clientsock,clientaddr)

if __name__ == '__main__':
	
	def go(a,b):
		print(b)
		print(isinstance(a,socket.socket))
		data=a.recv(1024)
		print(data.decode("utf-8"))
		a.send("我接收到了你的信息".encode("utf-8"))
		a.close()

	c=TCP_Server(("127.0.0.1",8848),go)