#/TCP/TCP_Client
#_*_coding:utf-8_*_

import threading
import socket


class TCP_Server(threading.Thread):
    """TCP服务端工具类"""

    def __init__(self, address, function, gamerData):
        """
        Args:
                address: 用于绑定TPC的地址和端口的元组
                function: 接口函数,或类,用于接收和处理客户端的连接
                gamerData: 玩家数据对象
        """

        super(TCP_Server, self).__init__()

        self.address = address
        self.function = function
        self.gamerData = gamerData

        self.serverTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverTCP.bind(self.address)
        self.serverTCP.listen(5)

        self.ClientList = []

        self.start()

    def run(self):
        flag = 0
        while True:
            clientsock, clientaddr = self.serverTCP.accept()

            threading.Thread(target=self.function, args=(
                clientsock, clientaddr, flag, self.gamerData, self)).start()

            flag += 1
            if flag > 999:
                flag -= 999

    def SandAll(self, tcp, data):
        """向全体用户转发消息"""
        for x in self.ClientList:
            if x is not tcp:
                x.sendData(data)
