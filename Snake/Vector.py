import math


class Vector(list):
    """向量计算类"""

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
        super(Vector, self).__init__([self.x, self.y])

    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)

    @classmethod
    def from_points(cls, a, b):
        return cls(b[0] - a[0], b[1] - a[1])

    def judge(self, p, size):
        """判断p点与本点之间的距离是否在size范围内"""
        b = self.get_distance(p)
        if size >= b:
            return True
        else:
            return False

    def get_distance(self, p):
        """返回p点与本点的距离"""
        a = Vector.from_points(self, p)
        return a.get_magnitude()

    def get_magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        magnitude = self.get_magnitude()
        self.x /= magnitude
        self.y /= magnitude
        self[0] = self.x
        self[1] = self.y
        return self

    def to_int(self):
        return (int)(self.x), (int)(self.y)

    def __add__(self, rhs):
        return Vector(self.x + rhs.x, self.y + rhs.y)

    def __sub__(self, rhs):
        return Vector(self.x - rhs.x, self.y - rhs.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)

    # def __eq__(self,V):
    # 	if self[]:
    # 		pass


if __name__ == '__main__':
    a = Vector(1, 2)
    b = Vector(3, 4)
    c = Vector(3, 6)
    print(b.judge(c, 4))
    print(Vector.from_points(a, c))
    print(a + b)
    print(b - a)
    print(a, b)
    print(a * 3)
    print(a / 2.)
    print(b.normalize())
    print(b, b[1])
    print(a[0])
    d = [[1, 2], [2, 3], [2, 1], [1, 2]]
    e = d[0]
    print(d)
    del e
    print(d)
