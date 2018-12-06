import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from logic.ddz import DouDiZhu
import logging
usernames = ["test0001", "test0002", "test0003"]
logging.basicConfig(level=logging.DEBUG,
                    format='{asctime} {levelname} {message}',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    style='{')

ddz = DouDiZhu(usernames, logging)
# ddz.do_xipai()
# ddz.do_fapai()
# ddz.plays = {
#     0: [0, 1, 2, 3, 4, 10, 11, 16, 19, 20, 22, 32, 34, 36, 45, 48, 50],
#     1: [6, 8, 13, 14, 15, 17, 21, 24, 27, 28, 29, 33, 35, 37, 39, 42, 43],
#     2: [5, 7, 9, 12, 18, 23, 25, 26, 30, 31, 38, 40, 41, 46, 47, 49, 51]
# }
# ddz.card_bt = [44, 52, 53]
# first = ddz.get_random_zddz_start()
# print("first:", ddz.do_zddz(first, False))

# second = first + 1
# if second > 2:
#     second = 0

# print("second", ddz.do_zddz(second, True))

# third = second + 1
# if third > 2:
#     third = 0


# print("first:", first)
# print("second:", second)
# print("third:", third)
# print("third", ddz.do_zddz(third, True))

# print(ddz.is_feiji([0,1,2, 4,5,6, 7,8,9]))

# print(ddz.is_feiji([4,5,6, 8,9,10]))

# print(ddz.is_feiji([0,1, 4,5,6, 8,9,10]))

# print(ddz.is_feiji([0,1, 4,5,6, 8,9,10, 28, 29]))
# print(ddz.is_feiji([0,1, 4,5,6, 8,9,10, 28, 32]))

# print(ddz.is_feiji([0,1, 4,5,6, 8,9,10, 28, 29]))
# print(ddz.is_feiji([32, 33, 34, 36, 37, 38, 40, 41, 44, 47]))
# print(ddz.cmp_feiji([0, [0,1, 4,5,6, 8,9,10, 28, 29], 'feiji'], [0, [32, 33, 34, 36, 37, 38, 40, 41, 44, 47] , 'feiji']))


ddz.get_tips([
    52,
    53,

    48,49,50,51
])