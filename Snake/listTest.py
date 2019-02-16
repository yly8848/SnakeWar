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

data = '[[413, 2917], [413, 2911], [413, 2905], [413, 2899], [413, 2893], [413, 2887], [413, 2881], [413, 2875], [413, 2869], [413, 2863], [413, 2857], [413, 2851], [413, 2845], [413, 2839], [413, 2833], [413, 2827], [413, 2821], [413, 2815], [413, 2809], [413, 2803], [413, 2797], [413, 2791], [413, 2785], [413, 2779], [413, 2773], [413, 2767]]'
print(json.loads(data))
