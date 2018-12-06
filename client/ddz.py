import random
import arrow

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

class DouDiZhu:
    '''
        发牌程序
    '''
    def __init__(self, usernames, logger):
        '''
            @array userames ["a", "b", "c"]
        '''
        self.logger = logger
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

        # 出牌记录
        self.chupai_record = []

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

        # 出牌统计
        self.chupai_count = 0

        # 抢地主
        self.zddz_first = -1

        # 抢地主回合
        self.zddz_bouts = []

        self.zddz_bouts_count = 1

        # 出牌
        self.chupai_first = -1

        # 出牌回合
        self.chupai_bouts = []

        # 玩家顺序
        self.usernames = usernames

        # 当前状态 "zddz" = 抢地主 "chupai" = 出牌 "over" = 结束
        self.mode = "zddz"

        self.errcode = 1

        self.errmessage = ''

        self.bout_start_time = None

    def do_timeout_auto_next(self, timeout=30, zddz_callback = None, chupai_callback = None):
        '''
            执行超时自动行为
        '''
        if self.mode == 'zddz':
            current_time = arrow.now()
            # self.logger.debug("do_timeout_auto_next zddz mode {0} {1} res={2}".format(current_time.timestamp, self.bout_start_time.timestamp, current_time.timestamp - self.bout_start_time.timestamp))
            if current_time.timestamp - self.bout_start_time.timestamp >= timeout:
                if len(self.zddz_bouts) == 0:
                    play_index = self.zddz_first
                else:
                    play_index = self.zddz_bouts[len(self.zddz_bouts) - 1][0]
                    if play_index + 1 > 2:
                        play_index = 0
                    else:
                        play_index = play_index + 1
                self.logger.debug("do_zddz: {0}".format(play_index))
                res = self.do_zddz(play_index = play_index, z = False)
                if zddz_callback:
                    zddz_callback(self, res)

        elif self.mode == 'chupai':
            current_time = arrow.now()
            if current_time.timestamp - self.bout_start_time.timestamp >= timeout:
                if chupai_callback:
                    chupai_callback(self)


    def get_random_zddz_start(self):
        '''
            随机开始
        '''
        self.zddz_first = random.randint(0, 2)
        self.bout_start_time = arrow.now()
        return self.zddz_first

    def do_xipai(self):
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

        self.user_card_used = {0:[], 1:[], 2: []}
        self.chupai_count = 0
        return self

    def do_fapai(self):
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
    
    def get_play_card(self, play_index=None):
        if play_index == None:
            return self.plays
        else:
            return self.plays[play_index]

    def get_play_index(self, username):
        return self.usernames.index(username)

    def get_play_name(self, play_index):
        return self.usernames[play_index]

    def do_zddz(self, play_index = -1, z = False):
        '''
            抢地主
            @int play_index 玩家索引值[0 - 2]
            @bool z 抢地主=True 不抢=False

            return
            @string bouts fail=本次操作失败 continue=继续  end_xaipai=结束并出牌 end_re_xaipai=结束并重新洗牌
            @int  plays_dz_index 等于-1等于抢地主回合结束
            @string errmessage 失败原因
        '''
        if isinstance(play_index, str):
            play_index = self.get_play_index(play_index)

        bouts = "continue" 
        # self.plays_dz_index = -1
        errmessage = None
        # 判断抢地主回合次数
        if len(self.zddz_bouts) >= 3:
            bouts = "fail"

        # 判断是否第一个抢地主
        if bouts != "fail" and len(self.zddz_bouts) == 0:
            if self.zddz_first == play_index:
                self.zddz_bouts.append([play_index, z])
            else:
                errmessage = "抢地主顺序不正确@1"
                bouts = "fail"

        elif bouts != "fail": # 判断第二或以上抢地主
            before_play_index = self.zddz_bouts[len(self.zddz_bouts) - 1][0]
            if before_play_index + 1 > 2:
                next_play_index = 0
            else:
                next_play_index = before_play_index + 1
                
            if next_play_index == play_index:
                self.zddz_bouts.append([play_index, z])
            else:
                errmessage = "抢地主顺序不正确@2 {0} {1}".format(next_play_index, play_index)
                bouts = "fail"

        # 判断抢地主回合是否完成
        if bouts != "fail" and len(self.zddz_bouts) == 3:
            for d in self.zddz_bouts:
                if d[1]:
                    bouts = "end_chupai"
                    self.plays_dz_index = d[0]
                    self.plays[self.plays_dz_index].extend(self.card_bt)
                    for index in self.plays:
                        self.user_card_unused[index] = self.plays[index].copy()
                    self.mode = 'chupai'

            # 回合结束
            if bouts == "continue":
                bouts = "end_re_xaipai"
            
            # 重发牌第二次，还有没有抢地主强制选第一
            if bouts == "end_re_xaipai" and self.zddz_bouts_count >= 2:
                self.plays_dz_index = self.zddz_first
                self.plays[self.plays_dz_index].extend(self.card_bt)
                for index in self.plays:
                    self.user_card_unused[index] = self.plays[index].copy()
                bouts = "end_chupai"
                self.mode = 'chupai'
            else:
                self.zddz_bouts = []
                # 执行重新洗牌/发牌
                self.do_xipai()
                self.do_fapai()

            if bouts == "end_re_xaipai":
                self.zddz_bouts_count = self.zddz_bouts_count + 1

        v = None
        if bouts == "continue":
            next_play_index = play_index + 1
            if next_play_index > 2:
                next_play_index = 0
            v = next_play_index
        elif bouts == "end_chupai":
            v = self.plays_dz_index
        elif bouts == "end_re_xaipai":
            v = self.zddz_first

        # 刷新回合时间
        if bouts != "fail":
            self.bout_start_time = arrow.now()
        return bouts, v, errmessage

    def get_card_bt(self):
        '''
            获取三张底牌
        '''
        return self.card_bt

    def do_sortcard(self):
        '''
            排序
        '''
        for p in self.plays:
            self.plays[p].reverse()
        return self

    def get_showcard(self, custom_card_list = None):
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
    
    def do_chupai(self, play_index, card_list):
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
                    message = '没有这个卡牌:{0} {1}'.format(self.get_showcard([card]), self.user_card_unused[play_index])
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
            z_card_list = self.get_showcard(card_list)
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
            z_card_list = self.get_showcard(card_list)
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
            z_card_list = self.get_showcard(card_list)
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
            z_card_list = self.get_showcard(card_list)
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
            z_card_list = self.get_showcard(card_list)
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
            z_card_list = self.get_showcard(card_list)
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
            z_card_list = self.get_showcard(card_list)
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
            z_card_list = self.get_showcard(card_list)
            count = dict_count(z_card_list)
            count_values = dict_value_to_list(count)
            if len(count) == 3 and 4 in count_values and (1 in count_values or 2 in count_values):
                allow = True

        return allow, None
