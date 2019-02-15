import pygame
from pygame.locals import *
from sys import exit
from random import *
import math


class CreatWindow(object):
    """游戏窗口控制类"""

    locat = [100, 100]  # 本地坐标
    maxspeed = 6  # 最大速度
    speed_xy = [maxspeed, 0]  # x,y方向的速度

    angle = 90  # 蛇头方向的偏转角度
    angle_speed=15 #蛇头转向时的速度

    direction = 4  # 方向,1 上,2 下,3 左,4 右

    snake = []  # 蛇身节点

    def __init__(self, size):

        self.size = size

        pygame.init()
        self.screen = pygame.display.set_mode(size, 0, 32)
        pygame.display.set_caption("Snake War")
        self.clock = pygame.time.Clock()

        self.snake = [(100, 100), (90, 100), (80, 100), (70, 100),
                      (60, 100), (50, 100), (40, 100), (30, 100), (20, 100), (10, 100), ]

    def setTick(self, fip=60):
        self.clock.tick(fip)

    def setBackground(self, img=None, pos=None):

        self.screen.fill((255, 255, 255))

        if img is not None:
            self.screen.blit(img, pos)

    def drawCircle(self, rp):
        rc = (43, 232, 2)
        #rp = (100, 100)
        rr = 10
        pygame.draw.circle(self.screen, rc, rp, rr)

    def drawSnake(self):
        for x in self.snake:
            self.drawCircle(x)

    def update(self):
        pygame.display.update()

    def ListionEvent(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

    def move(self):

        keys = pygame.key.get_pressed()

        L = keys[K_LEFT]
        R = keys[K_RIGHT]
        U = keys[K_UP]
        D = keys[K_DOWN]

        if L and self.direction != 4:
            self.direction = 3
            if self.angle < 90 or self.angle > 270:
                self.angle -= self.angle_speed
            elif self.angle < 270:
                self.angle += self.angle_speed

        if R and self.direction != 3:
            self.direction = 4
            if self.angle > 270 or self.angle < 90:
                self.angle += self.angle_speed
            elif self.angle > 90:
                self.angle -= self.angle_speed

        if U and self.direction != 2:
            self.direction = 1
            if self.angle > 180:
                self.angle -= self.angle_speed
            elif self.angle < 180:
                self.angle += self.angle_speed

        if D and self.direction != 1:
            self.direction = 2
            if self.angle > 180:
                self.angle += self.angle_speed
            elif self.angle > 0:
                self.angle -= self.angle_speed

        #偏转角度修正
        if self.angle > 360:
            self.angle = self.angle % 360
        if self.angle < 0:
            self.angle = 360 + self.angle

        #计算xy方向的速度
        self.locat[0] += (int)(self.maxspeed *
                               round(math.sin(math.pi * 2 * (self.angle / 360.)), 4))
        self.locat[1] += (int)(self.maxspeed *
                               round(math.cos(math.pi * 2 * (self.angle / 360.)), 4))

        #加入蛇身列表,移动蛇
        self.snake.insert(0, (self.locat[0], self.locat[1]))
        if len(self.snake) > 30:
            self.snake.pop()

        if self.locat[0] > 640:
            self.locat[0] = 0
        if self.locat[0] < 0:
            self.locat[0] = 640
        if self.locat[1] > 400:
            self.locat[1] = 0
        if self.locat[1] < 0:
            self.locat[1] = 400


if __name__ == '__main__':
    win = CreatWindow((640, 400))

    while True:
        win.setTick(30)
        win.setBackground()
        win.ListionEvent()

        win.drawSnake()
        win.move()

        win.update()
