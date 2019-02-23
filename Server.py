import time

from TCP.TCP_Server import *
from TCP.TCP_Client import *
from TCP.GamerData import *
from TCP.Server_getClient import *
from Snake.Roboter import *
from Snake.Vector import *


MapSize = [3000, 3000]
gamerData = GamerData(MapSize)

# ai = []
# for x in range(3):
#     a = AI('ai' + str(x), MapSize, 6, gamerData)
#     ai.append(a)

server = TCP_Server(("127.0.0.1", 8848), getClientSocket, gamerData)
# while True:
#     time.sleep(1 / 40)
#     for i in ai:
#         i.run(server)
