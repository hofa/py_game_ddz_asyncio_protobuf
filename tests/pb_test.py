import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from protocols import game_pb2


notify = game_pb2.GameZddzNotify()
# a = notify.player.add()
# a.username = "sb"
# a.card.extend([1, 2, 3, 4, 5])
# print(notify)
# a.card.extend([1, 2, 3, 4, 5])
# notify.usernames.extend("test0001")

# print(notify.usernames)
# b = list(a.card)
# print(b)

# res = notify.SerializeToString()
# print(res)

notify.END_CHUPAI