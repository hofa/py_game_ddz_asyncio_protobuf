import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from logic.ddz import DouDiZhu
usernames = ["test0001", "test0002", "test0003"]

ddz = DouDiZhu(usernames)
ddz.xipai()
ddz.fapai()

# first = ddz.random_zddz_start()
first = ddz.zddz_first = 0
print("开始:", usernames[first])


# res = ddz.zddz(1, False)
# print(res)

# res = ddz.zddz(0, False)
# print(res)
# res = ddz.zddz(1, False)
# print(res)
# res = ddz.zddz(2, False)
# print(res)


# res = ddz.zddz(0, False)
# print(res)
# res = ddz.zddz(1, True)
# print(res)
# res = ddz.zddz(2, False)
# print(res)

res = ddz.zddz("test0001", False)
print(res)