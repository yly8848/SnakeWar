import time

from TCP.TCP_Server import *
from TCP.TCP_Client import *
from TCP.GamerData import *
from TCP.Server_getClient import *
from Snake.Roboter import *
from Snake.Vector import *


MapSize = [3000, 3000]
gamerData = GamerData(MapSize)

server = TCP_Server(("127.0.0.1", 8848), getClientSocket, gamerData)

ai = []
for x in range(5):
    a = AI('ai' + str(x), MapSize, gamerData, 6)
    ai.append(a)

while True:
    time.sleep(1 / 40)
    for i in ai:
        i.letWeGo(server)
