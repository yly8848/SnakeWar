#_*_coding:utf-8_*_
import threading
import json
from random import *
import sys
sys.path.append(r"../")
from TCP.TCP_Server import *


class GamerData(object):
    """玩家数据存取类"""

    def __init__(self, MapSize):
        super(GamerData, self).__init__()
        self.MapSize = MapSize

        self.FoodList = []
        self.HeadList = {}
        self.AllPos = {}
        self.mutex = threading.Lock()

        self.initFood()

    def initFood(self):
        for x in range(200):
            self.addFood([randint(10, self.MapSize[0] - 10),
                          randint(10, self.MapSize[1] - 10)])

    def addGamer(self, name):
        self.HeadList[name] = [-1, -1, 8]
        self.AllPos[name] = []

    def upGamerData(self, name, data):
        self.HeadList[name] = data
        self.udData(name)

    def dieGamer(self, name, isAi=False, server=None):
        if isAi:
            size = len(self.AllPos[name])
            food = []
            for x in range(0, size, 3):
                self.addFood(self.AllPos[name][x])
                food.append(self.AllPos[name][x])
            data = {'message': 'addfood', 'addfood': food}
            datas = json.dumps(data)
            server.SandAll(None, datas)

        self.AllPos[name].clear()
        self.HeadList[name] = [-1, -1, 0]

    def delGamer(self, name):
        del self.HeadList[name]

    def addFood(self, pos):
        if self.mutex.acquire(1):
            if pos not in self.FoodList:
                self.FoodList.append(pos)
            self.mutex.release()

    def removeFood(self, pos):
        if self.mutex.acquire(1):
            if pos in self.FoodList:
                self.FoodList.remove(pos)

            if len(self.FoodList) < 100:
                for x in range(100):
                    self.addFood([randint(10, self.MapSize[0] - 10),
                                  randint(10, self.MapSize[1] - 10)])
            self.mutex.release()

    def udData(self, name):
        size = self.HeadList[name][2]
        x = self.HeadList[name][0]
        y = self.HeadList[name][1]
        self.AllPos[name].insert(0, [x, y])
        length = len(self.AllPos[name])
        if length > size:
            self.AllPos[name].pop()
