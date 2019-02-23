
import json
from TCP.TCP_Client import *
from Snake.MainWin import *
from Snake.PositionCalc import *


class Client():
    """客户端玩家类"""

    def __init__(self):
        super(Client, self).__init__()

        self.win = CreatWindow((640, 400))
        self.tcp = TCP_Client(("127.0.01", 8848),
                              self.getData, None, self.Close)

    def getData(self, data):
        try:
            j = json.loads(data)
            message = j['message']
            if message == 'init':
                food = j['food']
                self.win.food = food
            elif message == 'pos':
                pos = j['pos']
                self.win.upEnemy(pos)
            elif message == 'addfood':
                food = j['addfood']
                for x in food:
                    self.win.food.append(x)
                print("add food ++++++++++++", food)
            elif message == 'eatfood':
                food = j['eatfood']
                if food in self.win.food:
                    self.win.food.remove(food)
                print("eat food ------------", food)
            elif message == 'exit':
                name = j['name']
                self.win.delEnemy(name)

        except Exception as e:
            print("json解析错误")
            print(data)
            return

    def Close(self):
        print("服务器已关闭连接")


client = Client()

while True:
    client.win.setTick(40)

    client.win.setBackground()
    client.win.ListionEvent()

    client.win.dieJudge(client.tcp)
    client.win.move(client.tcp)

    client.win.drawEnemy()

    client.win.drawFood()
    client.win.drawSnake()

    client.win.update()
