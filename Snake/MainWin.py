#_*_coding:utf-8_*_

import pygame
from pygame.locals import *
from sys import exit
from random import *
import math
import time
import threading
import json

import sys
sys.path.append(r"../")
from Snake.PositionCalc import *
from TCP.TCP_Client import *


class CreatWindow(object):
    """游戏窗口控制类"""

    MapSize = [3000, 3000]  # 地图大小

    locat = [0, 0]  # 蛇头 本地窗口坐标
    Position = [300, 300]  # 蛇头 大地图坐标
    winPos = []  # 视野/窗口左上角位于大地图的坐标

    maxspeed = 6  # 最大速度
    speed_xy = [maxspeed, 0]  # x,y方向的速度

    angle = 180  # 蛇头方向的偏转角度 0~360
    angle_speed = 15  # 蛇头转向时的速度

    snake = []  # 蛇身节点
    length = 0
    food = []

    enemyDict = {}

    isDie = False

    def __init__(self, size):

        self.size = size

        pygame.init()
        self.screen = pygame.display.set_mode(size, 0, 32)
        pygame.display.set_caption("Snake War")
        self.background = pygame.image.load("./bg.jpg").convert()
        self.clock = pygame.time.Clock()

        self.calc = Calc(self.Position, self.locat, self.size)

        self.mutex = threading.Lock()

        self.initSnake()

    def initSnake(self):

        self.Position[0] = randint(100, self.MapSize[0] - 100)
        self.Position[1] = randint(100, self.MapSize[1] - 100)
        self.Position[0] = 200
        self.Position[1] = 1000
        self.locat[0] = self.size[0] // 2
        self.locat[1] = self.size[1] // 2
        self.winPos = self.calc.getWinPos()

        self.length = 10
        for x in range(10):
            self.snake.append((self.Position[0], self.Position[1] + x * 10))

    def setTick(self, fip=60):
        self.clock.tick(fip)

    def setBackground(self):

        self.screen.fill((0, 0, 0))

        x = 0 - self.winPos[0]
        y = 0 - self.winPos[1]
        self.screen.blit(self.background, (x, y))

    def drawCircle(self, rp, rc=(43, 232, 2)):
        #rp = (100, 100)
        rr = 10
        pygame.draw.circle(self.screen, rc, rp, rr)

    def drawSnake(self):

        for x in self.snake:
            if self.calc.rangeJudge(self.winPos, x):
                p = self.calc.getObjectPos(self.winPos, x)
                self.drawCircle(p)

    def drawFood(self):

        for x in self.food:
            if self.calc.rangeJudge(self.winPos, x):
                p = self.calc.getObjectPos(self.winPos, x)
                self.drawCircle(p, (123, 36, 241))

        # if len(self.food) < 30:
        #     for i in range(40):
        #         self.food.append(
        #             (randint(10, self.MapSize[0] - 10), randint(10, self.MapSize[1] - 10)))

    def upEnemy(self, data):
        if self.mutex.acquire(1):
            for x in data:
                if x not in self.enemyDict:
                    self.enemyDict[x] = []
                xx = data[x][0]
                yy = data[x][1]
                z = data[x][2]
                self.enemyDict[x].insert(0, [xx, yy])
                if z < len(self.enemyDict[x]):
                    self.enemyDict[x].pop()
                elif z == 0:
                    self.enemyDict[x].clear()
            self.mutex.release()

    def drawEnemy(self):
        if self.mutex.acquire(1):
            for x in self.enemyDict:
                for i in self.enemyDict[x]:
                    if self.calc.rangeJudge(self.winPos, i):
                        p = self.calc.getObjectPos(self.winPos, i)
                        self.drawCircle(p, (255, 36, 12))
        self.mutex.release()

    def delEnemy(self, name):
        name = str(name)
        if name in self.enemyDict:
            del self.enemyDict[name]

    def update(self):
        pygame.display.update()

    def ListionEvent(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:  # 空格加速
                    self.maxspeed = 15
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    self.maxspeed = 6

    def locatJudge(self):
        # locat位置判断,以及更新winPos,到达地图移动的效果

        a = self.size[0] // 5 * 2  # 左上角
        b = self.size[0] // 5 * 3  # 右上角
        c = self.size[1] // 5 * 2  # 左下角
        d = self.size[1] // 5 * 3  # 右下角

        # 到达边界时,限制视野移动
        if self.winPos[0] <= -100 or self.winPos[0] + self.size[0] >= self.MapSize[0] + 100 or self.winPos[1] <= -100 or self.winPos[1] + self.size[1] >= self.MapSize[1] + 100:

            if self.winPos[0] <= -100:
                self.winPos[1] += self.speed_xy[1]
                if self.speed_xy[0] > 0:
                    self.winPos[0] += self.speed_xy[0]
                else:
                    self.locat[0] += self.speed_xy[0]
            elif self.winPos[0] + self.size[0] >= self.MapSize[0] + 100:
                self.winPos[1] += self.speed_xy[1]
                if self.speed_xy[0] < 0:
                    self.winPos[0] += self.speed_xy[0]
                else:
                    self.locat[0] += self.speed_xy[0]
            elif self.winPos[1] <= -100:

                self.winPos[0] += self.speed_xy[0]
                if self.speed_xy[1] > 0:
                    self.winPos[1] += self.speed_xy[1]
                else:
                    self.locat[1] += self.speed_xy[1]
            elif self.winPos[1] + self.size[1] >= self.MapSize[1] + 100:
                self.winPos[0] += self.speed_xy[0]
                if self.speed_xy[1] < 0:
                    self.winPos[1] += self.speed_xy[1]
                else:
                    self.locat[1] += self.speed_xy[1]

        # 在地图范围内,locat超出给定的abcd范围,地图移动
        elif self.locat[0] <= a or self.locat[0] >= b or self.locat[1] <= c or self.locat[1] >= d:
            self.winPos = self.calc.getWinPos()

            x = self.locat[0] + self.speed_xy[0]
            y = self.locat[1] + self.speed_xy[1]

            if (self.locat[0] <= a and x > self.locat[0]) or (self.locat[0] >= b and x < self.locat[0]):
                self.locat[0] += self.speed_xy[0]
            if (self.locat[1] <= c and y > self.locat[1]) or (self.locat[1] >= d and y < self.locat[1]):
                self.locat[1] += self.speed_xy[1]

        # 在abcd范围内,地图视野不变
        else:
            self.locat[0] += self.speed_xy[0]
            self.locat[1] += self.speed_xy[1]

    def move(self, tcp):
        # 发送数据
        data = {'message': 'pos', 'head': self.Position, 'size': self.length}
        datas = json.dumps(data)
        tcp.sendData(datas)

        if self.isDie:
            return

        keys = pygame.key.get_pressed()

        if keys[K_LEFT]:
            if self.angle == 90:
                pass
            elif self.angle < 90 or self.angle > 270:
                self.angle -= self.angle_speed
            elif self.angle < 270:
                self.angle += self.angle_speed

        if keys[K_RIGHT]:
            if self.angle == 270:
                pass
            elif self.angle > 270 or self.angle < 90:
                self.angle += self.angle_speed
            elif self.angle > 90:
                self.angle -= self.angle_speed

        if keys[K_UP]:
            if self.angle == 0:
                pass
            elif self.angle > 180:
                self.angle -= self.angle_speed
            elif self.angle < 180:
                self.angle += self.angle_speed

        if keys[K_DOWN]:
            if self.angle == 180:
                pass
            elif self.angle > 180:
                self.angle += self.angle_speed
            elif self.angle > 0:
                self.angle -= self.angle_speed

        # 偏转角度修正
        if self.angle > 360:
            self.angle = self.angle % 360
        if self.angle < 0:
            self.angle = 360 + self.angle

        # 计算xy方向的速度
        self.speed_xy[0] = (int)(self.maxspeed *
                                 round(math.sin(math.pi * 2 * (self.angle / 360.)), 4))
        self.speed_xy[1] = (int)(self.maxspeed *
                                 round(math.cos(math.pi * 2 * (self.angle / 360.)), 4))
        self.locatJudge()

        self.Position[0] += self.speed_xy[0]
        self.Position[1] += self.speed_xy[1]

        # 碰撞检测
        flag = True
        for i in self.food:
            x = math.pow(self.Position[0] - i[0], 2)
            y = math.pow(self.Position[1] - i[1], 2)
            if math.sqrt(x + y) < 18:
                self.food.remove(i)
                data = {'message': 'eatfood', 'eatfood': i}
                datas = json.dumps(data)
                tcp.sendData(datas)  # 发送数据
                flag = False
                self.length += 1

        # 移动蛇
        self.snake.insert(0, (self.Position[0], self.Position[1]))
        if flag:
            self.snake.pop()

    def dieJudge(self, tcp):

        if self.isDie:
            return

        flag = False
        for x in self.enemyDict:
            for i in self.enemyDict[x]:
                x = math.pow(self.Position[0] - i[0], 2)
                y = math.pow(self.Position[1] - i[1], 2)
                if math.sqrt(x + y) < 18:
                    flag = True
                    break

        if flag or self.Position[0] <= 0 or self.Position[0] >= self.MapSize[0] or self.Position[1] <= 0 or self.Position[1] >= self.MapSize[1]:
            self.isDie = True
            print("you is die")
            self.length = 0

            eat = []
            # 变成养料
            for i in range(2, len(self.snake), 4):
                self.food.append(self.snake[i])
                eat.append(self.snake[i])

            # 发送数据
            data = {'message': 'addfood', 'addfood': eat}
            datas = json.dumps(data)
            tcp.sendData(datas)

            self.snake.clear()
            # 重生
            threading.Thread(target=self.relive).start()

    def relive(self):
        time.sleep(1)
        self.isDie = False
        # 随机出生点

        self.initSnake()


if __name__ == '__main__':
    win = CreatWindow((640, 400))

    while True:
        win.setTick(40)

        win.setBackground()
        win.ListionEvent()

        win.dieJudge()
        win.move()

        win.drawEnemy()

        win.drawFood()
        win.drawSnake()

        win.update()
