import random
from pprint import pprint
"""一次一人发一张牌"""
 
L = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
H = ['\u2660', '\u2663', '\u2665', '\u2666']
w1 = []
w2 = []
w3 = []
 
# P = ['X','x']
# for x in H:
#     for y in L:
#         s = x + y
#         P.append(s)

# print(P)
# R.shuffle(P)
 
# i = 1
# while i <= 17:
#     w1.append(P.pop())
#     w2.append(P.pop())
#     w3.append(P.pop())
#     i += 1
 
# print(w1)
# # input()
# print(w2)
# # input()
# print(w3)
# # input()
# print(P)

def dict_value_to_list(d):
    o = []
    for i in d:
        o.append(d[i])
    return o

def dict_get_key(d):
    o = []
    for i in d:
        o.append(i)
    
    o.sort()
    return o

def dict_count_equal(d, equal):
    for i in d:
        if d[i] != equal:
            return False
    return True

def dict_count(d, index=1):
    count = {}
    for z in d:
        if z[index] in count:
            count[z[index]] = count[z[index]] + 1
        else:
            count[z[index]] = 1
    return count

class DT:
    '''
        发牌程序
    '''

    def __init__(self):
        # 牌值
        self.card = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,
                19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,
                36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53]

        # 牌集合
        # self.card_set = ["3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A", "Z", "Joker"]
        
        # 花色集合
        # self.color_set = ["方片", "梅花", "红桃", "黑桃"]

        # 牌号定义
        self.card_list = {
            0: ["方片", "3", 0, 0],
            1: ["梅花", "3", 1, 0],
            2: ["红桃", "3", 2, 0],
            3: ["黑桃", "3", 3, 0],

            4: ["方片", "4", 0, 1],
            5: ["梅花", "4", 1, 1],
            6: ["红桃", "4", 2, 1],
            7: ["黑桃", "4", 3, 1],

            8: ["方片", "5", 0, 2],
            9: ["梅花", "5", 1, 2],
            10: ["红桃", "5", 2, 2],
            11: ["黑桃", "5", 3, 2],

            12: ["方片", "6", 0, 3],
            13: ["梅花", "6", 1, 3],
            14: ["红桃", "6", 2, 3],
            15: ["黑桃", "6", 3, 3],

            16: ["方片", "7", 0, 4],
            17: ["梅花", "7", 1, 4],
            18: ["红桃", "7", 2, 4],
            19: ["黑桃", "7", 3, 4],

            20: ["方片", "8", 0, 5],
            21: ["梅花", "8", 1, 5],
            22: ["红桃", "8", 2, 5],
            23: ["黑桃", "8", 3, 5],

            24: ["方片", "9", 0, 6],
            25: ["梅花", "9", 1, 6],
            26: ["红桃", "9", 2, 6],
            27: ["黑桃", "9", 3, 6],

            28: ["方片", "10", 0, 7],
            29: ["梅花", "10", 1, 7],
            30: ["红桃", "10", 2, 7],
            31: ["黑桃", "10", 3, 7],

            32: ["方片", "J", 0, 8],
            33: ["梅花", "J", 1, 8],
            34: ["红桃", "J", 2, 8],
            35: ["黑桃", "J", 3, 8],

            36: ["方片", "Q", 0, 9],
            37: ["梅花", "Q", 1, 9],
            38: ["红桃", "Q", 2, 9],
            39: ["黑桃", "Q", 3, 9],

            40: ["方片", "K", 0, 10],
            41: ["梅花", "K", 1, 10],
            42: ["红桃", "K", 2, 10],
            43: ["黑桃", "K", 3, 10],

            44: ["方片", "A", 0, 11],
            45: ["梅花", "A", 1, 11],
            46: ["红桃", "A", 2, 11],
            47: ["黑桃", "A", 3, 11],

            48: ["方片", "2", 0, 12],
            49: ["梅花", "2", 1, 12],
            50: ["红桃", "2", 2, 12],
            51: ["黑桃", "2", 3, 12],

            52: ["Black", "Joker", 4, 13],
            53: ["Red", "Joker", 5, 13]
        }

        # 洗牌记录 
        self.card_xipai = []

        # 三张底牌
        self.card_bt = []

        # 地主索引值
        self.plays_dz_index = -1

        # 玩家手牌记录
        self.plays = {0:[], 1:[], 2:[]}
    
    def xipai(self):
        '''
            洗牌
        '''
        self.card_xipai = self.card.copy()
        random.shuffle(self.card_xipai)
        self.card_bt = []
        self.plays = {0:[], 1:[], 2:[]}
        self.plays_dz_index = -1
        # print(self.card)
        # print(self.card_xipai)
        return self

    def fapai(self):
        '''
            发牌
        '''
        # 三张底牌
        self.card_bt.append(self.card_xipai.pop())
        self.card_bt.append(self.card_xipai.pop())
        self.card_bt.append(self.card_xipai.pop())

        # 发17张
        for i in range(0, 17):
            self.plays[0].append(self.card_xipai.pop())
            self.plays[1].append(self.card_xipai.pop())
            self.plays[2].append(self.card_xipai.pop())
        return self

    def qiangdizhu(self, play_index):
        '''
            抢地主
            @int play_index 玩家索引值[0 - 2]
        '''
        self.plays_dz_index = play_index
        self.plays[play_index].extend(self.card_bt)
        return self

    def sortcard(self):
        '''
            排序
        '''
        for p in self.plays:
            self.plays[p].sort()
        return self

    def showcard(self, custom_card_list = None):
        '''
            显示
        '''
        if custom_card_list == None:
            card_list = {}
            for p in self.plays:
                card_list[p] = []
                for s in self.plays[p]:
                    card_list_tmp = self.card_list[s].copy()
                    card_list_tmp.append(s)
                    card_list[p].append(card_list_tmp)
        else:
            card_list = []
            for s in custom_card_list:
                card_list_tmp = self.card_list[s].copy()
                card_list_tmp.append(s)
                card_list.append(card_list_tmp)

        return card_list
    

class DTP(DT):

    def __init__(self):
        super(DTP, self).__init__()
        # 出牌记录
        self.chupai_record = []

        # 玩家已出手牌
        self.user_card_used = {0:[], 1:[], 2: []}

        # 玩家未出手牌
        self.user_card_unused = {0:[], 1:[], 2: []}

        # 判断出牌类型
        self.type_func = [
            self.kongzhang,
            self.danzhang,
            self.duizhang,
            self.sanzhang,
            self.lianduizhang,
            self.shunzizhang,
            self.tonghuazhang,
            self.zhadanzhang,
            self.guizhadanzhang,
            self.sandaiyizhang,
            self.sidaiyizhang,
        ]

        self.chupai_count = 0

    def xipai2(self):
        '''
            洗牌
        '''
        self.xipai()
        self.user_card_used = {0:[], 1:[], 2: []}
        self.chupai_count = 0
        return self

    def qiangdizhu2(self, play_index):
        '''
            抢地主
        '''
        self.qiangdizhu(play_index)
        for index in self.plays:
            self.user_card_unused[index] = self.plays[index].copy()
        
        return self

    def chupai(self, play_index, card_list):
        '''
            出牌
        '''
        self.chupai_count = self.chupai_count + 1
        allow = True
        message = ''
        if len(card_list) >= 1:
            # 判断玩家是否拥有这个手牌
            for card in card_list:
                if not card in self.user_card_unused[play_index]:
                    message = '没有这个卡牌:{0} {1}'.format(self.showcard([card]), self.user_card_unused[play_index])
                    allow = False
                    break

            l1 = len(card_list)
            l2 = len(set(card_list))
            if l1 != l2:
                message = '出牌异常'
                allow = False

            card_list.sort()

        # 判断出牌是否符合规则， 并且得出出牌类型
        card_type = None
        if allow:
            allow = False
            for func in self.type_func:
                a, p = func(card_list)
                if a:
                    allow = True
                    card_type = func.__name__
                    break
            if not allow:
                message = "出牌不符合规则"

        # 加入出牌记录
        if allow:
            for card in card_list:
                self.user_card_unused[play_index].remove(card)
                self.user_card_used[play_index].append(card)
        return allow, message, card_type

    def kongzhang(self, card_list):
        '''
            空张判断
        '''
        allow = False
        if len(card_list) == 0:
            allow = True
        return allow, None

    def danzhang(self, card_list):
        '''
            单张判断
        '''
        allow = False
        if len(card_list) == 1:
            allow = True
        return allow, None

    def duizhang(self, card_list):
        '''
            对张判断
        '''
        allow = False
        if len(card_list) == 2:
            count = {}
            z_card_list = self.showcard(card_list)
            count = dict_count(z_card_list)
            if len(count) == 1:
                allow = True
        return allow, None

    def sanzhang(self, card_list):
        '''
            三张判断
        '''
        allow = False
        if len(card_list) == 3:
            count = {}
            z_card_list = self.showcard(card_list)
            count = dict_count(z_card_list)
            if len(count) == 1:
                allow = True
        return allow, None

    def lianduizhang(self, card_list):
        '''
            连对张判断
        '''
        allow = False
        if len(card_list) >= 6 and (52 not in card_list and 53 not in card_list):
            count = {}
            z_card_list = self.showcard(card_list)
            count = dict_count(z_card_list)
            # 每张只能出现二次
            if dict_count_equal(count, 2):
                count2 = dict_count(z_card_list, index=3)
                key2 = dict_get_key(count2)
                key2.reverse()
                first = key2[0]
                key2.remove(first)
                allow = True
                for k in range(0, len(key2)):
                    if first - k - key2[k] != 1:
                        allow = False
                        break
        return allow, None

    def shunzizhang(self, card_list):
        '''
            顺子张判断
        '''
        allow = False
        if len(card_list) >= 5 and (52 not in card_list and 53 not in card_list):
            count = {}
            z_card_list = self.showcard(card_list)
            count = dict_count(z_card_list)
            # 每张只能出现一次
            if dict_count_equal(count, 1):
                count2 = dict_count(z_card_list, index=3)
                key2 = dict_get_key(count2)
                key2.reverse()
                first = key2[0]
                key2.remove(first)
                allow = True
                for k in range(0, len(key2)):
                    if first - k - key2[k] != 1:
                        allow = False
                        break
        return allow, None

    def tonghuazhang(self, card_list):
        '''
            同花张判断
        '''
        allow = False
        if len(card_list) >= 5:
            count = {}
            z_card_list = self.showcard(card_list)
            count = dict_count(z_card_list, index=0)

            if len(count) == 1:
                allow = True

        return allow, None

    def zhadanzhang(self, card_list):
        '''
            炸弹判断
        '''
        allow = False
        if len(card_list) == 4:
            count = {}
            z_card_list = self.showcard(card_list)
            count = dict_count(z_card_list)
            if len(count) == 1:
                allow = True
        return allow, None

    def guizhadanzhang(self, card_list):
        '''
            鬼炸弹判断
        '''
        allow = False
        if len(card_list) == 2 and 52 in card_list and 53 in card_list:
            allow = True
        return allow, None

    
    def sandaiyizhang(self, card_list):
        '''
            三带一张判断
        '''
        allow = False
        if len(card_list) >= 4:
            count = {}
            z_card_list = self.showcard(card_list)
            count = dict_count(z_card_list)
            count_values = dict_value_to_list(count)
            if len(count) == 2 and 3 in count_values and (1 in count_values or 2 in count_values):
                allow = True

        return allow, None

    def sidaiyizhang(self, card_list):
        '''
            四带二张判断
        '''
        allow = False
        if len(card_list) >= 5:
            count = {}
            z_card_list = self.showcard(card_list)
            count = dict_count(z_card_list)
            count_values = dict_value_to_list(count)
            if len(count) == 3 and 4 in count_values and (1 in count_values or 2 in count_values):
                allow = True

        return allow, None

# hand = []
# for i in range(5):
#     cardFace = random.choice( cardFaces )
#     suite = random.choice( suites )
#     pickACard =str(cardFace) +" of "+ str(suite)
#     card = pickACard
#     hand.append(card)
# print(hand)

# 发牌
'''
    判断出牌
    1. 判断牌是否未出现过
    2. 判断单牌, 连牌, 对子, 连对, 炸弹， 
'''
dt = DT()
card = dt.xipai().fapai().qiangdizhu(1).sortcard().showcard()
# import pprint
# pprint.pprint(card)
# pprint.pprint(dt.card_xipai)
# pprint.pprint(dt.plays)
# print(card)
# print("length:", len(card[0]) + len(card[1]) + len(card[2]))

dtp = DTP()
# card = dtp.xipai2().fapai().qiangdizhu2(1).sortcard().showcard()
dtp.plays = {
    0: [0, 1, 2, 3, 4, 10, 11, 16, 19, 20, 22, 32, 34, 36, 45, 48, 50],
    1: [6, 8, 13, 14, 15, 17, 21, 24, 27, 28, 29, 33, 35, 37, 39, 42, 43, 44, 52, 53],
    2: [5, 7, 9, 12, 18, 23, 25, 26, 30, 31, 38, 40, 41, 46, 47, 49, 51]
}
play_index = 0
'''
{0: [['方片', '3', 0, 0, 0],
     ['梅花', '3', 1, 0, 1],
     ['红桃', '3', 2, 0, 2],
     ['黑桃', '3', 3, 0, 3],
     ['方片', '4', 0, 1, 4],
     ['红桃', '5', 2, 2, 10],
     ['黑桃', '5', 3, 2, 11],
     ['方片', '7', 0, 4, 16],
     ['黑桃', '7', 3, 4, 19],
     ['方片', '8', 0, 5, 20],
     ['红桃', '8', 2, 5, 22],
     ['方片', 'J', 0, 8, 32],
     ['红桃', 'J', 2, 8, 34],
     ['方片', 'Q', 0, 9, 36],
     ['梅花', 'A', 1, 11, 45],
     ['方片', '2', 0, 12, 48],
     ['红桃', '2', 2, 12, 50]],
 1: [['红桃', '4', 2, 1, 6],
     ['方片', '5', 0, 2, 8],
     ['梅花', '6', 1, 3, 13],
     ['红桃', '6', 2, 3, 14],
     ['黑桃', '6', 3, 3, 15],
     ['梅花', '7', 1, 4, 17],
     ['梅花', '8', 1, 5, 21],
     ['方片', '9', 0, 6, 24],
     ['黑桃', '9', 3, 6, 27],
     ['方片', '10', 0, 7, 28],
     ['梅花', '10', 1, 7, 29],
     ['梅花', 'J', 1, 8, 33],
     ['黑桃', 'J', 3, 8, 35],
     ['梅花', 'Q', 1, 9, 37],
     ['黑桃', 'Q', 3, 9, 39],
     ['红桃', 'K', 2, 10, 42],
     ['黑桃', 'K', 3, 10, 43],
     ['方片', 'A', 0, 11, 44],
     ['Black', 'Joker', 4, 13, 52],
     ['Red', 'Joker', 5, 13, 53]],
 2: [['梅花', '4', 1, 1, 5],
     ['黑桃', '4', 3, 1, 7],
     ['梅花', '5', 1, 2, 9],
     ['方片', '6', 0, 3, 12],
     ['红桃', '7', 2, 4, 18],
     ['黑桃', '8', 3, 5, 23],
     ['梅花', '9', 1, 6, 25],
     ['红桃', '9', 2, 6, 26],
     ['红桃', '10', 2, 7, 30],
     ['黑桃', '10', 3, 7, 31],
     ['红桃', 'Q', 2, 9, 38],
     ['方片', 'K', 0, 10, 40],
     ['梅花', 'K', 1, 10, 41],
     ['红桃', 'A', 2, 11, 46],
     ['黑桃', 'A', 3, 11, 47],
     ['梅花', '2', 1, 12, 49],
     ['黑桃', '2', 3, 12, 51]]}
'''

# 判断牍
if False:
    dtp.qiangdizhu2(play_index)
    card_list = [6]
    res = dtp.chupai(0, card_list)
    print(res)

    dtp.qiangdizhu2(play_index)
    card_list = [0, 6]
    res = dtp.chupai(0, card_list)
    print(res)

# 四带二
if False:
    dtp.qiangdizhu2(play_index)
    card_list = [0, 1, 2, 3, 4, 36]
    res = dtp.chupai(0, card_list)
    print(res)
    card = dtp.showcard(card_list)
    pprint(card)

# 空牌
if False:
    dtp.qiangdizhu2(play_index)
    card_list = []
    res = dtp.chupai(0, card_list)
    print(res)
    card = dtp.showcard(card_list)
    pprint(card)

# 一牌
if False:
    dtp.qiangdizhu2(play_index)
    card_list = [0]
    res = dtp.chupai(0, card_list)
    print(res)
    card = dtp.showcard(card_list)
    pprint(card)

# 对牌
if False:
    dtp.qiangdizhu2(play_index)
    card_list = [0, 1]
    res = dtp.chupai(0, card_list)
    print(res)
    card = dtp.showcard(card_list)
    pprint(card)

# 三张
if False:
    dtp.qiangdizhu2(play_index)
    card_list = [0, 1, 2]
    res = dtp.chupai(0, card_list)
    print(res)
    card = dtp.showcard(card_list)
    pprint(card)

# 三带一张
if False:
    dtp.qiangdizhu2(play_index)
    card_list = [0, 1, 2, 36]
    res = dtp.chupai(0, card_list)
    print(res)
    card = dtp.showcard(card_list)
    pprint(card)

    dtp.qiangdizhu2(play_index)
    card_list = [0, 1, 2, 36, 10, 11]
    res = dtp.chupai(0, card_list)
    print(res)
    card = dtp.showcard(card_list)
    pprint(card)

# 顺子
if False:
    play_index = 2
    dtp.qiangdizhu2(play_index)
    card_list = [5, 9, 12, 18, 23, 25]
    res = dtp.chupai(play_index, card_list)
    print(res)
    card = dtp.showcard(card_list)
    pprint(card)


class Tips:

    def get_min(self, card_list):
        pass
    
    def get_max(self, before_card_list, card_list):
        pass

    def find(self):
        pass
    
    