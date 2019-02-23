import math
import json

data = '{"data":[1,2,4],"size":1}'
a = json.loads(data)
print(a["data"], type(a["data"]))
size = a['size']
print(size, type(size))

mylist = [(1, 3), (5, 6)]
b = json.dumps(mylist)
print(b, type(b))

c = json.loads(b)
print(c, type(c))

a = {'dsf': 123, 'data': [3, 5, 6]}
b = a.copy()
del b['dsf']
print(a, b)
c = 123
print(str(c))

a = [[3, 6], [3, 5]]
b = [[12, 4], [36, 3], [345, 634]]
print(a + b)
a.append(b)
print(b[2:6])
print(a is not a)

a = {"sdf": 234, "dsf": 3254}
