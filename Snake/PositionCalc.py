#_*_coding:utf-8_*_


class Calc(object):
    """坐标位置计算判断类"""

    def __init__(self, Position, locat, WinSize):
        super(Calc, self).__init__()
        self.Position = Position
        self.locat = locat
        self.WinSize = WinSize

    def getWinPos(self):
        x = self.Position[0] - self.locat[0]
        y = self.Position[1] - self.locat[1]
        return [x, y]

    def rangeJudge(self, winpos, pos):
        """判断点 pos 是否在窗口显示范围之内
        Args:
                winpos: 显示窗口左上角的坐标
                pos: 要判断的二维坐标点
        Returns:
                pos在范围内返回true,否则返回false
        """
        if pos[0] >= winpos[0] and pos[0] <= winpos[0] + self.WinSize[0]:
            if pos[1] >= winpos[1] and pos[1] <= winpos[1] + self.WinSize[1]:
                return True
        return False

    def getObjectPos(self, winpos, pos):
        """把点pos的大地图坐标转化为窗口内的坐标
        Args:
                winpos: 显示窗口左上角的坐标
                pos: 要判断的二维坐标点
        Returns:
                返回该点相对于窗口位置的坐标[x,y]
        """
        x = pos[0] - winpos[0]
        y = pos[1] - winpos[1]
        return [x, y]
