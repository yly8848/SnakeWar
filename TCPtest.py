import json
import sys
sys.path.append(r"./")

from TCP import TCP_Server, TCP_Client
from Server import Server

sys.path.append(r"./Snake/")

import MainWin
import PositionCalc


mypos = []
getpos = []


def getPos(data):
    pass


def Close(): print("server is close")


tcp = TCP_Client.TCP_Client(("127.0.0.1", 8848), getPos, Close)

win = MainWin.CreatWindow((640, 400))
while True:
    win.setTick(40)
    win.setBackground()
    win.ListionEvent()

    win.move()
    win.drawSnake()
    win.drawFood()

    tcp.sendData(json.dumps(win.snake))

    win.update()
