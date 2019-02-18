import math
import json

data = '{"data":[1,2,4]}'
a = json.loads(data)
print(a["data"], type(a["data"]))

mylist = [(1, 3), (5, 6)]
b = json.dumps(mylist)
print(b, type(b))

c = json.loads(b)
print(c, type(c))

d = "aaa"
print(d + "sdf")

e = {1: 'a', 3: 'fff', 'aaa': 'haha'}

e[2] = 'dsf'

for x in e:
    if x != 'aaa':
        print(e[x])
del e[2]

print(e)


a = 5.9
b = 6
c = 8
d = 9
print(a * .1)
