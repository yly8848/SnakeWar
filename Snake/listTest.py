import math

a = (1, 2)
b = (3, 4)
c = (1, 2)
mylist = [a, b]

print(mylist[1])

mylist.append((6, 6))
mylist.insert(0, (7, 7))

mylist.pop()

print(a == c)
for x in mylist:
    print(x[1], x[0])


print(math.pi)
print(math.sin(math.pi * 2 * (45 / 360)))
print(math.sin(math.pi * 2 * (90 / 360)))
print(round(math.sin(math.pi * 2), 4))
print(math.sin(math.pi * 2 * (298 / 360)))

print((-10 % 360))
