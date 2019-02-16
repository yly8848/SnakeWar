#_*_coding:utf-8_*_

import sys
sys.path.append(r"../")

from TCP import TCP_Server, TCP_Client

datalist = {}


class getClientSocket(object):
    """服务器 接收 客户端请求 控制类"""

    def __init__(self, clientsock, clientaddr, flag):
        super(getClientSocket, self).__init__()

        self.address = clientaddr
        self.flag = flag

        self.tcp = TCP_Client.TCP_Client(
            None, self.getData, clientsock, self.Close)

    def getData(self, data):
        datalist[self.flag] = data
        print(datalist)
        self.tcp.sendData(datalist[0])

    def Close(self):
        # del datalist[self.flag]
        print(self.flag, "is close")


if __name__ == '__main__':

    TCP_Server.TCP_Server(("127.0.0.1", 8848), getClientSocket)
