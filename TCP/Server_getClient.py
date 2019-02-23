#_*_coding:utf-8_*_
import json
import sys
sys.path.append(r"../")
from TCP.TCP_Server import *
from TCP.TCP_Client import *
from TCP.GamerData import *


class getClientSocket(object):
    """服务器接收客户端请求 控制类"""

    def __init__(self, clientsock, clientaddr, flag, gamerData, Server):
        super(getClientSocket, self).__init__()

        self.address = clientaddr
        self.flag = flag
        self.gamerData = gamerData

        self.tcp = TCP_Client(
            None, self.getData, clientsock, self.Close)

        self.Server = Server
        self.Server.ClientList.append(self.tcp)

        # 加入数据队列
        self.gamerData.addGamer(self.flag)

        # 向客户端发送全部食物的位置
        init = {"message": "init", "food": self.gamerData.FoodList}
        initdata = json.dumps(init)
        self.tcp.sendData(initdata)

    def getData(self, data):

        self.Case(data)
        self.sendpos()

    def Close(self):
        self.gamerData.delGamer(self.flag)
        print(self.flag, "is close")

    def sendpos(self):
        headpos = self.gamerData.HeadList.copy()
        del headpos[self.flag]
        data = {"message": "pos", "pos": headpos}
        datas = json.dumps(data)
        self.tcp.sendData(datas)

    def Case(self, data):
        try:
            j = json.loads(data)
            message = j['message']

            if message == 'pos':
                head = j['head']
                size = j['size']
                head.append(size)
                self.gamerData.upGamerData(self.flag, head)

            elif message == 'eatfood':
                eat = j['eatfood']
                self.gamerData.removeFood(eat)

                data = {"message": "eatfood", "eatfood": eat}
                datas = json.dumps(data)
                self.Server.SandAll(self.tcp, datas)

            elif message == 'addfood':
                self.gamerData.dieGamer(self.flag)
                add = j['addfood']
                for x in add:
                    self.gamerData.addFood(x)

                data = {'message': 'addfood', 'addfood': add}
                datas = json.dumps(data)
                self.Server.SandAll(self.tcp, datas)
                print("++++++++++++++++++", datas)

        except Exception as e:
            print(self.flag, 'json解析错误')
            return
