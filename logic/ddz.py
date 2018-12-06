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

def dict_max_value_index(d):
    max_value = 0
    max_index = -1
    for z in d:
        if d[z] > max_value:
            max_index = z
    return max_value, max_index

def list_equal(a, b):
    for i in a:
        if i not in b:
            return False
    return True

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
        self.card_category = {
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

        self.card_ts = {
            "3": 0,
            "4": 1,
            "5": 2,
            "6": 3,
            "7": 4,
            "8": 5,
            "9": 6,
            "10": 7,
            "J": 8,
            "Q": 9,
            "K": 10,
            "A": 11,
            "2": 12,
            "Joker": 13,
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

        # 出牌最后记录
        # self.chupai_last_record = []

        # 玩家已出手牌
        self.user_card_used = {0:[], 1:[], 2: []}

        # 玩家未出手牌
        self.user_card_unused = {0:[], 1:[], 2: []}
        # 出牌记录
        self.card_record = []
        # 最后出牌
        self.last_card = []

        # 判断出牌类型
        self.type_func = [
            self.is_kongzhang,
            self.is_danzhang,
            self.is_duizhang,
            self.is_sanzhang,
            self.is_lianduizhang,
            self.is_shunzizhang,
            self.is_tonghuazhang,
            self.is_zhadanzhang,
            self.is_guizhadanzhang,
            self.is_sandaiyizhang,
            self.is_sidaiyizhang,
            self.is_feiji,
        ]
        
        # 比较大小
        self.cmp_func = [
            self.cmp_kongzhang,
            self.cmp_danzhang,
            self.cmp_duizhang,
            self.cmp_sanzhang,
            self.cmp_lianduizhang,
            self.cmp_shunzizhang,
            self.cmp_tonghuazhang,
            self.cmp_zhadanzhang,
            self.cmp_guizhadanzhang,
            self.cmp_sandaiyizhang,
            self.cmp_sidaiyizhang,
            self.cmp_feiji,
        ]

        # 权值
        self.weight_category = {
            "danzhang": 1, # 单张
            "duizhang": 2, # 对张
            "sanzhang": 3, # 三张 
            "lianduizhang": 4, # 连对
            "shunzizhang": 5, # 顺子
            "sandaiyizhang": 3, # 三带一/三带二
            "sidaiyizhang": 5, # 四带二
            "feiji": 6, # 飞机
            "zhadanzhang": 7, # 炸弹
            "guizhadanzhang": 7, # 鬼炸
        }

        # 出牌统计
        # self.chupai_count = 0

        # 抢地主
        self.zddz_first = -1

        # 抢地主回合
        self.zddz_bouts = []

        self.zddz_bouts_count = 1

        self.current_zddz_index = -1
        self.current_zddz_z = False

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

        self.current_chupai_index = -1
        self.current_chupai_card = []

        self.context = None
        self.context_index = None

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
                    play_index, bout_first = self.get_current_ready_chupai_play_index()
                    if bout_first:
                        self.user_card_unused[play_index].sort()
                        res = self.do_chupai(play_index, [self.user_card_unused[play_index][0]])
                    else:
                        res = self.do_chupai(play_index, [])
                    # self.check_game_over()
                    chupai_callback(self, res)


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
        # self.chupai_count = 0
        self.chupai_bouts = []
        self.zddz_bouts = []
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
                    # print(d, self.plays_dz_index)


            
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
            elif bouts == "end_re_xaipai":
                self.zddz_bouts = []
                # 执行重新洗牌/发牌
                self.do_xipai()
                self.do_fapai()

            if bouts == "end_re_xaipai":
                self.zddz_bouts_count = self.zddz_bouts_count + 1

            # 抢地主完成
            if bouts == "end_chupai":
                self.logger.debug("确定地主: {0} {1} {2}".format(self.zddz_bouts, self.plays_dz_index, self.get_play_name(self.plays_dz_index)))
                self.logger.debug("usernames: {0}".format(self.usernames))
                pass

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
            self.current_zddz_index = play_index
            self.current_zddz_z = z

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

    def get_showcard(self, custom_card = None):
        '''
            显示
        '''
        if custom_card == None:
            card = {}
            for p in self.plays:
                card[p] = []
                for s in self.plays[p]:
                    card_tmp = self.card_category[s].copy()
                    card_tmp.append(s)
                    card[p].append(card_tmp)
        else:
            card = []
            for s in custom_card:
                card_tmp = self.card_category[s].copy()
                card_tmp.append(s)
                card.append(card_tmp)

        return card
    
    def get_chupai_record(self):
        return self.chupai_record
    
    def get_current_ready_chupai_play_index(self):
        '''
            取出准备出牌的玩家索引值
            return
            @int current_chupai_play_index 返回细索引值
            @bool bouts_first 回合开始
            # @array context 上一个玩家
        '''
        current_chupai_play_index = -1
        # 回合开始
        bouts_first = False
        # 上文值
        # context = None
        chupai_bouts_count = len(self.chupai_bouts)
        if chupai_bouts_count == 0:
            current_chupai_play_index = self.plays_dz_index
            bouts_first = True
        elif chupai_bouts_count:
            chupai_bouts = self.chupai_bouts[chupai_bouts_count - 1]
            if chupai_bouts == 3:
                for i in chupai_bouts:
                    if len(chupai_bouts[i][1]) > 0:
                        current_chupai_play_index = chupai_bouts[i][0]
                        bouts_first = True
            else:
                l = len(self.chupai_bouts[chupai_bouts_count - 1])
                end_chupai_play_index = self.chupai_bouts[chupai_bouts_count - 1][l - 1][0]

                
                # for i in self.chupai_bouts[chupai_bouts_count - 1]:
                #     if len(i[1]) > 0:
                #         context = i
                #self.logger.debug("chupai_bouts {0} i={1}".format(self.chupai_bouts[chupai_bouts_count - 1], i))

                current_chupai_play_index = end_chupai_play_index + 1
                if current_chupai_play_index > 2:
                    current_chupai_play_index = 0

        if self.context_index != None and current_chupai_play_index == self.context_index:
            bouts_first = True
        # return current_chupai_play_index, bouts_first, context
        return current_chupai_play_index, bouts_first

    def do_chupai(self, play_index = -1, card = []):
        '''
            出牌
        '''
        # self.logger.info("play_index: {0} username: {1}".format(play_index, self.usernames))
        card = list(card)
        if isinstance(play_index, str):
            play_index = self.get_play_index(play_index)
        # 回合判断
        current_ready_chupai_play_index, bouts_first = self.get_current_ready_chupai_play_index()
        
        if len(card) > 0:
            card.reverse()

        allow = True
        message = ''
        if current_ready_chupai_play_index != play_index:
            allow = False
            message = "出牌顺序不正确 current_ready_chupai_play_index={0} play_index={1} self.plays_dz_index={2}".format(current_ready_chupai_play_index, play_index, self.plays_dz_index)

        # self.chupai_count = self.chupai_count + 1
        
        if allow and len(card) >= 1:
            # 判断玩家是否拥有这个手牌
            for c in card:
                if not c in self.user_card_unused[play_index]:
                    message = '没有这个卡牌:{0} {1}'.format(self.get_showcard([c]), self.user_card_unused[play_index])
                    allow = False
                    break

            l1 = len(card)
            l2 = len(set(card))
            if l1 != l2:
                message = '出牌异常'
                allow = False

            card.sort()

        # 判断出牌是否符合规则， 并且得出出牌类型
        card_type = None
        if allow:
            allow = False
            for func in self.type_func:
                a, p = func(card)
                if a:
                    allow = True
                    card_type = func.__name__.replace("is_", "")
                    break
            if not allow:
                message = "出牌不符合规则"

        
        # 非回合开始对比上文
        if allow and bouts_first == False:
            card_type_cmp_func = "cmp_" + card_type
            func = getattr(self, card_type_cmp_func)
            if self.context_index != None and self.context != None and self.context_index != play_index and func(self.context, [play_index, card, card_type]) == False:
                allow = False
                message = "牌值少于上家 context={0} current={1}".format(self.context, [play_index, card, card_type])
            
        # 回合开始的第一个人不允许出空牌
        if allow and bouts_first and len(card) == 0:
            allow = False
            message = "请出牌"

        # 加入出牌记录
        if allow:
            for c in card:
                self.user_card_unused[play_index].remove(c)
                self.user_card_used[play_index].append(c)

            # 出牌回合数据加入
            chupai_bouts_count = len(self.chupai_bouts)
            
            if chupai_bouts_count == 0:
                self.chupai_bouts.append([[play_index, card, card_type]])
            elif (chupai_bouts_count - 1) in self.chupai_bouts and self.chupai_bouts[chupai_bouts_count - 1] == 3:
                self.chupai_bouts.append([[play_index, card, card_type]])
            else:
                self.chupai_bouts[chupai_bouts_count - 1].append([play_index, card, card_type])

            # 记录当前出牌
            self.current_chupai_card = card
            self.current_chupai_index = play_index
            self.chupai_record.extend(card)

            # 上文信息记录
            if len(card) > 0:
                self.context = [play_index, card, card_type]
                self.context_index = play_index
        return allow, message

    def check_game_over(self):
        '''
            检查游戏是否结束
        '''
        over = False
        win_index = None
        for play_index in self.user_card_unused:
            if len(self.user_card_unused[play_index]) == 0:
                over = True
                win_index = play_index
                self.mode = "gameover"
                break
        return over, win_index


    def is_kongzhang(self, card):
        '''
            空张判断
        '''
        allow = False
        if len(card) == 0:
            allow = True
        return allow, None

    def is_danzhang(self, card):
        '''
            单张判断
        '''
        allow = False
        if len(card) == 1:
            allow = True
        return allow, None

    def is_duizhang(self, card):
        '''
            对张判断
        '''
        allow = False
        if len(card) == 2 and 53 not in card:
            count = {}
            z_card = self.get_showcard(card)
            count = dict_count(z_card)
            if len(count) == 1:
                allow = True
        return allow, None

    def is_sanzhang(self, card):
        '''
            三张判断
        '''
        allow = False
        if len(card) == 3:
            count = {}
            z_card = self.get_showcard(card)
            count = dict_count(z_card)
            if len(count) == 1:
                allow = True
        return allow, None

    def is_lianduizhang(self, card):
        '''
            连对张判断
        '''
        allow = False
        if len(card) >= 6 and (52 not in card and 53 not in card):
            count = {}
            z_card = self.get_showcard(card)
            count = dict_count(z_card)
            # 每张只能出现二次
            if dict_count_equal(count, 2):
                count2 = dict_count(z_card, index=3)
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

    def is_shunzizhang(self, card):
        '''
            顺子张判断
        '''
        allow = False
        if len(card) >= 5 and (52 not in card and 53 not in card):
            count = {}
            z_card = self.get_showcard(card)
            count = dict_count(z_card)
            # 每张只能出现一次
            if dict_count_equal(count, 1):
                count2 = dict_count(z_card, index=3)
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

    def is_tonghuazhang(self, card):
        '''
            同花张判断
        '''
        allow = False
        if len(card) >= 5:
            count = {}
            z_card = self.get_showcard(card)
            count = dict_count(z_card, index=0)

            if len(count) == 1:
                allow = True

        return allow, None

    def is_zhadanzhang(self, card):
        '''
            炸弹判断
        '''
        allow = False
        if len(card) == 4:
            count = {}
            z_card = self.get_showcard(card)
            count = dict_count(z_card)
            if len(count) == 1:
                allow = True
        return allow, None

    def is_guizhadanzhang(self, card):
        '''
            鬼炸弹判断
        '''
        allow = False
        if len(card) == 2 and 52 in card and 53 in card:
            allow = True
        return allow, None

    def is_sandaiyizhang(self, card):
        '''
            三带一张判断
        '''
        allow = False
        if len(card) >= 4:
            count = {}
            z_card = self.get_showcard(card)
            count = dict_count(z_card)
            count_values = dict_value_to_list(count)
            if len(count) == 2 and 3 in count_values and (1 in count_values or 2 in count_values):
                allow = True

        return allow, None

    def is_sidaiyizhang(self, card):
        '''
            四带二张判断
        '''
        allow = False
        count = None
        if len(card) >= 5:
            count = {}
            z_card = self.get_showcard(card)
            count = dict_count(z_card)
            count_values = dict_value_to_list(count)
            if len(count) == 3 and 4 in count_values and (1 in count_values or 2 in count_values):
                allow = True
            
        return allow, None

    def is_feiji(self, card):
        '''
            飞机
        '''
        allow = False
        count = None
        if len(card) >= 6:
            allow = True
            count = {}
            z_card = self.get_showcard(card)
            count = dict_count(z_card)
            for k in count:
                # 2以上牌面不能组成飞机
                if self.card_ts[k] > 11:
                    allow = False
                    break

            if allow: 
                count_values = dict_value_to_list(count)
                # 获取最大的值是3还是4
                max_value_count = max(count_values)
                if max_value_count < 3:
                    allow = False

            if allow:
                #  获取最小值
                min_value_count = min(count_values)
                if max_value_count == min_value_count:
                    min_value_count = -1

                max_value_list = []
                min_value_list = []
                for v in count:
                    if count[v] == max_value_count:
                        max_value_list.append(self.card_ts[v])
                    
                    if count[v] == min_value_count:
                        min_value_list.append(v)

                # 判断大值连续
                max_value_list.sort()
                for p in range(0, len(max_value_list)):
                    if p + 1 < len(max_value_list):
                        if max_value_list[p] + 1 != max_value_list[p + 1]:
                            allow = False
                            break
                
                if min_value_count > -1:
                    allow = False
                    if len(card) - len(max_value_list) * max_value_count == len(max_value_list):
                        allow = True
                    
                    if len(count) == len(max_value_list) + len(min_value_list):
                        allow = True
                        num = min_value_list[0]
                        v = count[num]
                    
                        for c in count:
                            if count[c] >= 3:
                                continue
                            
                            if count[c] != v:
                                allow = False
        return allow, None
    
    def cmp_kongzhang(self, old, new):
        '''
            空张
        '''
        return True

    def cmp_danzhang(self, old, new):
        '''
            单张比较
        '''
        output = False
        if old[2] == 'danzhang' and old[2] == new[2]:
            if new[1][0] > old[1][0]:
                output = True
        return output

    def cmp_duizhang(self, old, new):
        '''
            对张判断
        '''
        output = False
        if old[2] == 'duizhang' and old[2] == new[2]:
            if new[1][0] > old[1][0]:
                output = True
        return output

    def cmp_sanzhang(self, old, new):
        '''
            三张判断
        '''
        output = False
        if old[2] == 'sanzhang' and old[2] == new[2]:
            if new[1][0] > old[1][0]:
                output = True
        return output

    def cmp_lianduizhang(self, old, new):
        '''
            连对张判断
        '''
        output = False
        if old[2] == 'lianduizhang' and old[2] == new[2]:
            if new[1][0] > old[1][0] and len(new[1]) == len(old[1]):
                output = True
        return output

    def cmp_shunzizhang(self, old, new):
        '''
            顺子张判断
        '''
        output = False
        if old[2] == 'shunzizhang' and old[2] == new[2]:
            if new[1][0] > old[1][0] and len(new[1]) == len(old[1]):
                output = True
        return output

    def cmp_tonghuazhang(self, old, new):
        '''
            同花张判断
        '''
        output = False
        if old[2] == 'tonghuazhang' and old[2] == new[2]:
            if new[1][0] > old[1][0] and len(new[1]) == len(old[1]):
                output = True
        return output

    def cmp_zhadanzhang(self, old, new):
        '''
            炸弹判断
        '''
        output = False
        if old[2] == 'zhadanzhang' and old[2] == new[2]:
            if new[1][0] > old[1][0] and len(new[1]) == len(old[1]):
                output = True
        
        if old[2] != 'guizhadanzhang' and old[2] != 'zhadanzhang':
            output = True

        return output

    def cmp_guizhadanzhang(self, old, new):
        '''
            鬼炸
        '''
        return True

    def cmp_sandaiyizhang(self, old, new):
        '''
            三带一张判断
        '''
        output = False
        if old[2] == 'sidaiyizhang' and old[2] == new[2]:
            old_count = dict_count(self.get_showcard(old[1]))
            old_count_list = dict_value_to_list(old_count)
            max_old_value, max_old_index = dict_max_value_index(old_count)

            new_count = dict_count(self.get_showcard(new[1]))
            new_count_list = dict_value_to_list(new_count)
            max_new_value, max_new_index = dict_max_value_index(new_count)

            if list_equal(old_count_list, new_count_list) and max_new_value > max_old_value and len(new[1]) == len(old[1]):
                output = True
        
        return output

    def cmp_sidaiyizhang(self, old, new):
        '''
            四带二张判断
        '''
        output = False
        if old[2] == 'sidaiyizhang' and old[2] == new[2]:
            old_count = dict_count(self.get_showcard(old[1]))
            old_count_list = dict_value_to_list(old_count)
            max_old_value, max_old_index = dict_max_value_index(old_count)

            new_count = dict_count(self.get_showcard(new[1]))
            new_count_list = dict_value_to_list(new_count)
            max_new_value, max_new_index = dict_max_value_index(new_count)

            if list_equal(old_count_list, new_count_list) and max_new_value > max_old_value and len(new[1]) == len(old[1]):
                output = True
        
        return output

    def cmp_feiji(self, old, new):
        '''
            飞机判断
        '''
        output = False
        if old[2] == 'feiji' and old[2] == new[2] and len(old[1]) == len(new[1]):
            old_count = dict_count(self.get_showcard(old[1]))
            new_count = dict_count(self.get_showcard(new[1]))

            old_count_value = dict_value_to_list(old_count)
            new_count_value = dict_value_to_list(new_count)
            old_count_value.sort()
            new_count_value.sort()
            if old_count_value == new_count_value:
                new_max_value = []
                old_max_value = []
                for a in new_count:
                    if new_count[a] == new_count_value[len(new_count_value) - 1]:
                        new_max_value.append(self.card_ts[a])
                
                for a in old_count:
                    if old_count[a] == old_count_value[len(old_count_value) - 1]:
                        old_max_value.append(self.card_ts[a])

                if max(new_max_value) > max(old_max_value):
                    output = True
        return output
    
    def get_tips(self, card, context=None):
        '''
            取得提示
            @array context [0, [1,2, 3], 'type']
        '''
        count_dict = {}
        d = self.get_showcard(card)
        d_c = dict_count(d)
        self.logger.debug(d)
        self.logger.debug(d_c)
        if context == None:
            pass
        else:
            pass

    def is_have_danzhang(self, card):
        '''
            单张
        '''
        pass
    
    def is_have_lianduizhang(self, card):
        '''
            连对张
        '''
        pass

    def is_have_duizhang(self, card):
        '''
            对张
        '''
        pass

    def is_have_shunzizhang(self, card):
        '''
            顺子
        '''
        pass
    
    def is_have_tonghuazhang(self, card):
        '''
            同花
        '''
        pass

    def is_have_zhadanzhang(self, card):
        '''
            炸
        '''
        pass

    def is_have_feiji(self, card):
        '''
            飞机
        '''
        pass

    def is_have_sanzhang(self, card):
        '''
            三张判断
        '''
        pass

    def is_have_guizhadanzhang(self, card):
        '''
            鬼炸
        '''
        pass

    def is_have_sandaiyizhang(self, card):
        '''
            三带一
        '''
        pass


    def is_have_sidaiyizhang(self, card):
        '''
            四带二
        '''
        pass