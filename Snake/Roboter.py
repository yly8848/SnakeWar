import time
import threading
from Vector import Vector
from random import *


class AI(object):
    """人机类,主要控制机器蛇的各种行为
            Args:
                    MapSize: 地图大小,人机的活动范围
                    speed: 人机的移动速度
                    food: 食物坐标list
                    enemy: 敌人,障碍物坐标
    """
    length = 8  # ai snake长度
    speed_xy = Vector(1, 1)
    eat_food = None  # 即将要吃的食物
    direc = None  # 要移动的方向

    isDie = False
    flag = False

    def __init__(self, MapSize, speed, food, enemy):
        super(AI, self).__init__()
        self.MapSize = MapSize
        self.speed = speed
        self.food = food
        self.enemy = enemy

        self.Head = Vector(
            randint(100, self.MapSize[0] - 100), randint(100, self.MapSize[1] - 100))

    def getHead(self):
        return self.Head

    def run(self):

        if self.isDie:
            return
        if self.dieJudge():
            return

        # 在食物列表里选一个最近的食物,利用冒泡法
        if self.eat_food is None:
            mini = [999, 0]
            len_f = len(self.food)
            for i in range(0, len_f):
                n = self.Head.get_distance(self.food[i])
                if n < mini[0]:
                    mini[0] = n
                    mini[1] = i

            self.eat_food = self.food[mini[1]]
            # 确定方向
            self.direc = Vector.from_points(self.Head, self.eat_food)
            self.direc.normalize()

        # 向食物方向移动 head -> food
        self.Head = self.Head + (self.direc * self.speed)

        if self.eat_food not in self.food:
            self.eat_food = None
            return

        # 食物 碰撞检测
        if self.Head.judge(self.eat_food, 18):
            self.food.remove(self.eat_food)
            self.eat_food = None
            self.length += 1

    def dieJudge(self):
        for x in self.enemy:
            if self.Head.judge(x, 18):
                self.isDie = True
                self.flag = True
                threading.Thread(target=self.Wait).start()
                return True
        return False

    def Wait(self):
        time.sleep(1)
        self.isDie = False
        self.Head = Vector(
            randint(100, self.MapSize[0] - 100), randint(100, self.MapSize[1] - 100))
        self.length = 8
        self.eat_food = None


if __name__ == '__main__':
    food = [[200, 200], [268, 200], [359, 440], [22, 65]]
    a = AI([1000, 1000], 6, food, [[0, 0]])
    while len(a.food) >= 2:
        a.run()
        time.sleep(0.1)
    print(len(food), len(a.food), food)
