import sys
import time
import json
import threading
from random import *
sys.path.append(r"../")
from Snake.Vector import *
from TCP.GamerData import *
from TCP.TCP_Server import *


class AI(threading.Thread):
    """人机类,主要控制机器蛇的各种行为

    """
    length = 8  # ai snake长度
    speed_xy = Vector(1, 1)
    eat_food = None  # 即将要吃的食物
    direc = None  # 要移动的方向

    isDie = False

    def __init__(self, name, MapSize, gamerData, speed,):
        """Args:
                    name: ai的名字
                    MapSize: 地图大小,人机的活动范围
                    gamerData: 所有玩家数据
                    speed: 人机的移动速度
        """
        super(AI, self).__init__()
        self.name = name
        self.MapSize = MapSize

        self.gamerData = gamerData
        self.food = gamerData.FoodList

        self.speed = speed

        self.gamerData.addGamer(self.name)

        self.Head = Vector(
            randint(100, self.MapSize[0] - 100), randint(100, self.MapSize[1] - 100))

    def getHead(self):
        return self.Head

    def letWeGo(self, server):
        if self.isDie:
            return
        if self.dieJudge(server):
            return

        # 在食物列表里选一个最近的食物,
        if self.eat_food is None:
            mini = [999, 0]
            len_f = len(self.food)
            for i in range(0, len_f):
                try:
                    n = self.Head.get_distance(self.food[i])
                    if n < mini[0]:
                        mini[0] = n
                        mini[1] = i
                except Exception as e:
                    mini[1] = 0
                    break

            self.eat_food = self.food[mini[1]]
            # 确定方向
            self.direc = Vector.from_points(self.Head, self.eat_food)
            self.direc.normalize()

        # 向食物方向移动 head -> food
        self.Head = self.Head + (self.direc * self.speed)
        # 保存数据
        self.gamerData.upGamerData(
            self.name, [(int)(self.Head[0]), (int)(self.Head[1]), self.length])

        if self.eat_food not in self.food:
            self.eat_food = None
            return

        # 食物 碰撞检测
        if self.Head.judge(self.eat_food, 18):
            self.gamerData.removeFood(self.eat_food)

            data = {'message': 'eatfood', 'eatfood': self.eat_food}
            datas = json.dumps(data)
            server.SandAll(None, datas)

            self.eat_food = None
            self.length += 1

    def dieJudge(self, server):
        for x in self.gamerData.AllPos:
            if x != self.name:
                for i in self.gamerData.AllPos[x]:
                    if self.Head.judge(i, 18):
                        self.isDie = True
                        self.gamerData.dieGamer(self.name, True, server)
                        threading.Thread(target=self.Wait).start()
                        return True
        return False

    def Wait(self):
        time.sleep(2)
        self.isDie = False
        self.Head = Vector(
            randint(100, self.MapSize[0] - 100), randint(100, self.MapSize[1] - 100))
        self.length = 8
        self.eat_food = None
