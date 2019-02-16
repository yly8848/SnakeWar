import json
import sys
sys.path.append(r"./")

from TCP import TCP_Server, TCP_Client
from Server import Server

sys.path.append(r"./Snake/")

import MainWin
import PositionCalc


class AAAA(object):
    """docstring for AAAA"""

    def __init__(self):
        super(AAAA, self).__init__()
        self.tcp = TCP_Client.TCP_Client(
            ("127.0.0.1", 8848), self.getPos, self.Close)
        self.win = MainWin.CreatWindow((640, 400))
        self.win.maxspeed = 0
        self.win.locat = [320, 200]

    def getPos(self, data):
        try:
            self.win.snake = json.loads(data)

        except Exception as e:
            return None

    def Close(self):
        print("server is close")


a = AAAA()

while True:
    a.win.setTick(40)
    a.win.setBackground()
    a.win.ListionEvent()

    # win.move()
    a.win.drawSnake()
    a.win.drawFood()

    a.win.winPos = [a.win.snake[0][0] - 320, a.win.snake[0][1] - 200]

    a.tcp.sendData("[]")

    a.win.update()
