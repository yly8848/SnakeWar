#/TCP/TCP_Client
#_*_coding:utf-8_*_

import threading
import socket

class TCP_Client(threading.Thread):
	"""TCP客户端工具类,"""

	__SIZE=2048 #接收数据的长度
	__isConnect=1 #是否已创建已有连接

	def __init__(self, address=None,function=None,client=None):
		"""
			如果是客户端用的话,填前面两个参数,连接服务器
			如果是服务端用的话,填后面两个参数,进行数据处理
			
		Args:
			addrs: 要连接的服务器地址族
			function: 函数接口,用于处理从服务器接收的数据
			client: socket,从服务端得到的socket客户端对象

		"""

		super(TCP_Client, self).__init__()
		
		if address is not None:
			self.address = address 
			self.clientTCP=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			self.__isConnect=self.clientTCP.connect_ex(self.address)

		elif client is not None and isinstance(client,socket.socket):
			self.__isConnect=0
			self.clientTCP=client

		self.function=function

		self.start()


	def run(self):

		while self.__isConnect==0:
			data=self.clientTCP.recv(self.__SIZE);
			if not data: break 						#Python的recv有些不一样,连接断开了还会接收到空的字符
			self.function(data.decode("utf-8"))


	def sendData(self,data):
		"""向已连接的服务器发送数据
			
		Args:
			data: 欲发送的数据

		Returns:
			如果当前对象还没有连接上服务器,返回False
			发送成功返回True
			其他的话,等着报错

		"""

		if self.__isConnect!=0:
			return False

		if type(data)==type(''):
			self.clientTCP.sendall(data.encode("utf-8"))
			return True


if __name__ == '__main__':
	
	ppp=lambda str:print(str)

	tcp=TCP_Client(("127.0.0.1",8848),ppp)
	a=tcp.sendData("ffff")
	print(a)
