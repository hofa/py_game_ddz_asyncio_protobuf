import tkinter as tk
import arrow
# from controller import *
import controller
from urllib.request import urlopen
from PIL import Image, ImageTk
import io
import hashlib
import os
from functools import partial
import ui
# def loadImageForUrl(url):
#     image_bytes = urlopen(url).read()
#     data_stream = io.BytesIO(image_bytes)
#     pil_image = Image.open(data_stream)
#     tk_image = ImageTk.PhotoImage(pil_image)
#     return tk_image

def down_for_url(url):
    name = ".".join(url.split(".")[0:-1])
    ext = url.split('.')[-1]
    hash = hashlib.md5()
    hash.update(bytes(name,encoding='utf-8'))
    md5 = hash.hexdigest()
    file_path = os.path.dirname(os.path.realpath(__file__)) + "/images/" + md5 + '.' + ext
    if not os.path.exists(file_path):
        file = open(file_path, "wb")
        file.write(urlopen(url).read())
        file.close()

    return file_path

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.after(500, lambda: master.switch_frame(PageLogin))

class PageLogin(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        title = tk.Label(self, text = '登录系统')
        title.pack()

        username = tk.Entry(self, background = 'white')
        username.pack()
        username.focus_set()
        

        password = tk.Entry(self, background = 'white')
        password.pack()
        
        login_action = controller.LoginController(master)
        login = tk.Button(self, text = '登录', command=lambda: login_action.do_request(username.get(), password.get()))
        # login = tk.Button(self, text = '登录', command=lambda: master.client.send(username.get(), password.get()))
        login.pack(side = tk.LEFT)

        register = tk.Button(self, text = '没有账号?', command=lambda: master.switch_frame(PageRegister))
        register.pack(side = tk.RIGHT)


        showtime = tk.Label(self, text="")
        showtime.pack(side = tk.BOTTOM)
        # self.count = 1 
        self.refresh_time(showtime)

        if master.client.default_username == None:
            username.insert(0, "test0001")
        else:
            username.insert(0, master.client.default_username)
            self.after(200, lambda: self.auto_login(login_action, username, password))
        password.insert(0, "a123456")

    def auto_login(self, login_action, username, password):
        login_action.do_request(username.get(), password.get())

    def refresh_time(self, label):
        # self.count = self.count + 1
        t = arrow.now()
        label["text"] = t.format("YYYY-MM-DD HH:mm:ss")
        self.after(500, self.refresh_time, label)

class PageRegister(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        title = tk.Label(self, text = '注册账号')
        title.pack()

        username = tk.Entry(self, background = 'white')
        username.pack()
        username.focus_set()

        password = tk.Entry(self, background = 'white')
        password.pack()

        register_action = controller.RegisterController(master)
        register = tk.Button(self, text = '注册', command=lambda: register_action.do_request(username.get(), password.get()))
        register.pack(side = tk.LEFT)

        returnLogin = tk.Button(self, text = '返回登录', command=lambda: master.switch_frame(PageLogin))
        returnLogin.pack(side = tk.RIGHT)


class PageHall(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        title = tk.Label(self, text = '游戏大厅')
        title.pack()
        room_list_action = controller.RoomListController(master)
        room_list_action.do_request()


class PageRoom(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        title = tk.Label(self, text = '房间:' + master.entry_room_name)
        title.pack()

        self.tips = tk.Label(self, text = '当前排队人数: 0')
        self.tips.pack()
        
        leave_room_action = controller.LeaveRoomController(master)
        button = tk.Button(self, text = '退出排队', command=lambda: leave_room_action.do_request())
        button.pack()

        entry_room_action = controller.EntryRoomController(master)
        entry_room_action.do_request(self.master.entry_room_id)



class PageGameDDZ(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, width=1024, height=800)
        self.master = master

        self.left_card = []
        self.right_card = []
        self.bottom_card = []
        self.change_card = []
        # 锁牌
        self.lock = True

        # 抢地主
        self.bottom_zddz_btns = []
        self.bottom_zddz_label = None
        self.left_zddz_label = None
        self.right_zddz_label = None

        self.left = None
        self.right = None
        self.top = None
        self.bottom = None
        self.center = None

        self.username = None
        self.place = None
        self.zddz_timeout = 30
        
        self.places = {}
        self.left_username = None
        self.right_username = None
        self.bottom_username = None
        # 底牌按钮组
        self.card_bt_btns = []
        # 打牌按钮组
        self.btns = []

        # 倒计时
        self.jobs = None

        self.ph = ui.PH()
        self.ph.fetch_all()

        self.configure(background="#211f20")
        self.right_card_num = 0
        self.left_card_num = 0
        self.bottom_card_num = []
        # self.initialize_lockers()
        self.center_card_num = []
        self.center_card = []

        self.win = None


    def append_show_center_card(self, card):
        xj = 45
        yj = 60
        for c in card:
            self.center_card_num.append(c)
            lenght = len(self.center_card_num)
            button = tk.Label(self.center, image=self.ph.cache[c])
            y = lenght % 100 / 10
            g = lenght % 10
            button.place(x=30 + g * 30, y=120 + yj * y)
            button.configure(background='#211f20')
            self.center_card.append(button)
   
    def caipai(self, z=False):
        '''
            出牌
        '''
        card = []
        if z:
            
            for btn in self.change_card:
                card.append(btn.card_id)
                # btn.destroy()
        else:
            # for btn in self.change_card:
            #     btn.is_change = False
            #     btn.place(y = 60)
            # self.change_card = []
            pass

        action = controller.GameChupaiController(self.master)
        # if z and len(self.change_card) > 0:
        #     action.do_request(card)
        # elif not z:
        #     action.do_request(card)
        action.do_request(card)
        # self.master.logger.debug("出牌 {0}".format())

    def init_btns(self):
        button = tk.Button(self.bottom, text = "出牌", width=6, command=lambda: self.caipai(True))
        button.place(x=400, y=160)
        self.btns.append(button)

        button = tk.Button(self.bottom, text = "不出", width=6, command=lambda: self.caipai(False))
        button.place(x=530, y=160)
        self.btns.append(button)

        button = tk.Button(self.bottom, text = "提示", width=6)
        button.place(x=930, y=60)
        self.btns.append(button)

        button = tk.Button(self.bottom, text = "托管", width=6, command=self.show_gameover_board)
        button.place(x=930, y=100)
        self.btns.append(button)
        self.lock = False

    def remove_btns(self):
        self.lock = True
        for btn in self.btns:
            btn.destroy()

    # def unlock(self):
    #     '''
    #         解锁
    #     '''
    #     self.lock = False

    def add_change(self, place):
        '''
            选择牌
        '''
        self.master.logger.debug("place {0} add_change_len:{1}".format(place, len(self.change_card)))
        if self.lock:
            return
     
        try:
            btn = None
            for b in self.bottom_card:
                if place == b.card_id:
                    btn = b
                    break
            # print(btn)
            if not btn.is_change:
                btn.is_change = True
                btn.place(y = 30)
                self.change_card.append(btn)
                # self.master.logger.debug("+ {0} {1} {2}".format(btn['text'], btn.winfo_rootx(), btn.winfo_rooty()))
            else:
                btn.is_change = False
                btn.place(y = 60)
                self.change_card.remove(btn)
                # self.master.logger.debug("- {0}".format(btn['text']))
        except Exception as e:
            self.master.logger.error(e)

    def card_bt_clear(self):
        '''
            清空底牌显示
        '''
        for btn in self.card_bt_btns:
            btn.destroy()


    def show_card_bt(self, card):
        '''
            显示底牌
        '''
        button = tk.Label(self.center, text = "底牌", bg="gray")
        button.place(x=0, y=0)
        self.card_bt_btns.append(button)
        j = 0
        for c in card:
            button = tk.Label(self.center, image=self.ph.cache[c])
            button.place(x=30 + j * 30, y=0)
            button.configure(background='#211f20')
            self.card_bt_btns.append(button)
            j = j + 1

    def dd(self, dd):
        for d in dd:
            d.destroy()
        dd = []

    def refresh_zddz_after_card(self, place):
        '''
            抢完地主刷新牌
        '''
        jf = 20
        jf2 = 40
        if place == 'left':
            self.dd(self.left_card)
            for i in range(0, self.left_card_num):
                button = tk.Label(self.left, image=self.ph.left_b_cache)
                button.image = self.ph.left_b_cache
                button.place(x=20, y=40 + jf * i)
                button.configure(background='#211f20')
                self.left_card.append(button)

        if place == 'right':
            self.dd(self.right_card)
            for i in range(0, self.right_card_num):
                button = tk.Label(self.right, image=self.ph.right_b_cache)
                button.image = self.ph.right_b_cache
                button.place(x=60, y=40 + jf * i)
                button.configure(background='#211f20')
                self.right_card.append(button)

        if place == 'bottom':
            # self.dd(self.bottom_card)
            self.show_bottom_card()

    def show_caipai_count_down(self, place, timeout):
        '''
            显示出牌倒计时
        '''
        self.zddz_clear()
        self.zddz_timeout = timeout
        
        if place == "left":
            self.left_zddz_label = tk.Label(self.left, text="30", bd=1)
            self.left_zddz_label.place(x=150, y=210)

        if place == "right":
            self.right_zddz_label = tk.Label(self.right, text="30", bd=1)
            self.right_zddz_label.place(x=20, y=210)

        if place == "bottom":
            self.bottom_zddz_label = tk.Label(self.bottom, text="30", bd=1)
            self.bottom_zddz_label.place(x=550 - 50, y=10)
            self.bottom_zddz_btns.append(self.bottom_zddz_label)

        self.zddz_time_refresh(place)

    def stop_caipai_count_down(self, place):
        self.after_cancel(self.jobs)
        if self.left_zddz_label != None and place == "left":
            self.left_zddz_label.destroy()
            self.left_zddz_label = None

        if self.right_zddz_label != None and place == "right":
            self.right_zddz_label.destroy()
            self.right_zddz_label = None

        if self.bottom_zddz_label != None and place == "bottom":
            self.bottom_zddz_label.destroy()
            self.bottom_zddz_label = None

    def zddz_time_refresh(self, place):
        '''
            抢地主计时器
        '''
        self.zddz_timeout = self.zddz_timeout - 1
        if self.left_zddz_label != None and place == "left":
            self.left_zddz_label["text"] = str(self.zddz_timeout)

        if self.right_zddz_label != None and place == "right":
            self.right_zddz_label["text"] = str(self.zddz_timeout)

        if self.bottom_zddz_label != None and place == "bottom":
            self.bottom_zddz_label["text"] = str(self.zddz_timeout)

        if self.zddz_timeout > 0:
            self.jobs = self.after(1000, self.zddz_time_refresh, place)

    def zddz_clear(self):
        '''
            清空斗地主
        '''
        self.zddz_timeout = 0
        if self.jobs != None:
            self.after_cancel(self.jobs)
            self.jobs = None

        if self.left_zddz_label:
            self.left_zddz_label.destroy()
            self.left_zddz_label = None

        if self.right_zddz_label:
            self.right_zddz_label.destroy()
            self.right_zddz_label = None

        if self.bottom_zddz_label:
            for btn in self.bottom_zddz_btns:
                btn.destroy()
            self.bottom_zddz_label = None

    def zddz(self, place, timeout = 30):
        '''
            抢地主
        '''
        self.zddz_clear()
        self.zddz_timeout = timeout
        
        if place == "left":
            self.left_zddz_label = tk.Label(self.left, text="30", bd=1)
            self.left_zddz_label.place(x=150, y=210)

        if place == "right":
            self.right_zddz_label = tk.Label(self.right, text="30", bd=1)
            self.right_zddz_label.place(x=20, y=210)

        if place == "bottom":
            self.bottom_zddz_label = tk.Label(self.bottom, text="30", bd=1)
            self.bottom_zddz_label.place(x=550 - 50, y=10)
            self.bottom_zddz_btns.append(self.bottom_zddz_label)
            game_ddz_action = controller.GameZddzController(self.master)
            button = tk.Button(self.bottom, text="抢地主", command=lambda:game_ddz_action.do_request(True))
            button.place(x=470 - 50, y=10)
            self.bottom_zddz_btns.append(button)
            button = tk.Button(self.bottom, text="不抢", command=lambda:game_ddz_action.do_request(False))
            button.place(x=580 - 50, y=10)
            self.bottom_zddz_btns.append(button)
        
        self.zddz_time_refresh(place)

    def show_bottom_card(self):
        self.master.logger.debug("show_bottom_card {0}".format(self.bottom_card_num))
        jf2 = 43
        # l = 0
        self.bottom_card_num.sort()
        # for q in self.bottom_card_num:
        #     button = tk.Label(self.bottom, image=self.ph.cache[q])
        #     # partial(self.add_change, q)
        #     button.bind('<Button-1>', lambda e, q = q:self.add_change(q))
        #     button.image = self.ph.cache[q]
        #     button.place(x=20 + l * jf2, y=60)
        #     button.is_change = False
        #     button.card_id = q
        #     button.configure(background='#211f20')
        #     self.bottom_card.append(button)
        #     l = l + 1

        len1 = len(self.bottom_card_num)
        len2 = len(self.bottom_card)
        if len2 > len1:
            for i in range(0, len2 - len1):
                btn = self.bottom_card.pop()
                btn.destroy()
        elif len2 < len1:
            for i in range(0, len1 - len2):
                button = tk.Label(self.bottom, image=self.ph.cache[99])
                # partial(self.add_change, q)
                # button.bind('<Button-1>', lambda e, q = q:self.add_change(q))
                # button.image = self.ph.cache[q]
                button.place(x=20 + (i + len2) * jf2, y=60)
                # button.is_change = False
                # button.card_id = q
                button.configure(background='#211f20')
                self.bottom_card.append(button)
        i = 0
        # self.master.logger.debug(self.bottom_card_num)
        # self.master.logger.debug(self.bottom_card)
        # return
        for q in self.bottom_card_num:
            button = self.bottom_card[i]
            button.unbind('<Button-1>')
            button.bind('<Button-1>', lambda e, q = q:self.add_change(q))
            button.is_change = False
            button.card_id = q
            button.configure(image=self.ph.cache[q])
            button.image = self.ph.cache[q]
            button.place(y=60)
            i = i + 1

    def init(self, pb_res):
        username = pb_res.username
        # index = list(pb_res.usernames).index(username)
        index = -1
        i = 0
        
        for s in pb_res.player:
            if s.username == username:
                index = i
                break
            i = i + 1

        # bottom = tk.Label(self, text = pb_res.player[index].username)
        # bottom.pack(side = tk.BOTTOM)

        if index + 1 <= 2:
            next_index = index + 1
        else:
            next_index = 0

        # right = tk.Label(self , text = pb_res.player[next_index].username)
        # right.pack(side = tk.RIGHT)

        if next_index + 1 <= 2:
            next_next_index = next_index + 1
        else:
            next_next_index = 0

        # left = tk.Label(self , text = pb_res.player[next_next_index].username)
        # left.pack(side =  tk.LEFT)

        # self.master.logger.debug("cur:{0} index: {1} next_index:{2} next_next_index:{3}".format(username, index, next_index, next_next_index))
        # master_width = 1024
        # top = tk.Frame(self, width=master_width, height=50, bg='black')
        # left = tk.Frame(self, width=50, height=master_width - 2 * 50, bg='blue')
        # center = tk.Frame(self, width=master_width  - 2 * 50, height=master_width - 2 * 50, bg='white')
        # right = tk.Frame(self, width=50, height=master_width - 2 * 50, bg='gray')
        # bottom = tk.Frame(self, width=200, height=200, bg='red')

        # top.grid(row=0, column=0)
        # left.grid(row=1, column=0)
        # center.grid(row=1, column=1)
        # right.grid(row=1, column=2)
        # bottom.grid(row=2, column=0)

        master_width = 1024
        master_height = 800
        top = tk.Frame(self, width=master_width, height=50, bg='black')
        left = tk.Frame(self, width=200, height=master_height  - 50 - 200, bg='white')
        center = tk.Frame(self, width=master_width  - 2 * 200, height=master_height - 50 - 200, bg='gray')
        right = tk.Frame(self, width=200, height=master_height  - 50 - 200, bg='white')
        bottom = tk.Frame(self, width=master_width, height=200, bg='white')
        # left
        username = tk.Label(left, text = pb_res.player[next_next_index].username)
        username.place(x=10, y=0)
        self.left_username = username
        self.left_card_num = pb_res.player[next_next_index].card_num
        self.right_card_num = pb_res.player[next_next_index].card_num
        # 间隔值
        # jf = 20
        # for i in range(0, pb_res.player[next_next_index].card_num):
        #     button = tk.Button(left, text = "", width=10)
        #     button.place(x=20, y=20 + jf *i)
        #     self.left_card.append(button)

        # right
        username = tk.Label(right, text = pb_res.player[next_index].username)
        username.place(x=100, y=0)
        # for i in range(0, pb_res.player[next_next_index].card_num):
        #     button = tk.Button(right, text = "", width=10)
        #     button.place(x=60, y=20 + jf *i)
        #     self.right_card.append(button)
        self.right_username = username

        self.master.logger.debug("right num: %d" % pb_res.player[next_next_index].card_num)

        jf2 = 40
        # bottom
        username = tk.Label(bottom, text = pb_res.player[index].username)
        username.place(x=10, y=0)
        # l = 0
        # for i in pb_res.card:
        #     button = tk.Button(bottom, text = str(i), width=3, command=partial(self.add_change, l))
        #     button.place(x=20 + l * jf2, y=60)
        #     button.is_change = False
        #     button.card_id = i
        #     self.bottom_card.append(button)
        #     l = l + 1

        

        self.bottom_username = username



        # center
        # button = tk.Label(center, text = "A", width=4, bg="gray")
        # button.place(x=0, y=0)
        # button = tk.Label(center, text = "B", width=4, bg="gray")
        # button.place(x=30, y=0)
        # self.master.logger.debug(".....")

        top.place(relx=0, rely=0)
        left.place(x=0, y=50)
        center.place(x=200, y=50)
        right.place(x=824, y=50)
        bottom.place(x=0, y=600)

        right.configure(background="#211f20")
        left.configure(background="#211f20")
        top.configure(background="#211f20")
        bottom.configure(background="#211f20")
        center.configure(background="#211f20")
        self.right = right
        self.left = left
        self.top = top
        self.bottom = bottom
        self.center = center
        
        self.places = {
            "left": pb_res.player[next_next_index].username, 
            "right": pb_res.player[next_index].username, 
            "bottom":  pb_res.player[index].username
        }

        for place in self.places:
            if self.places[place] == pb_res.first:
                self.zddz(place)
                break

        self.bottom_card_num = pb_res.card
        self.refresh_zddz_after_card("left")
        self.refresh_zddz_after_card("right")
        self.refresh_zddz_after_card("bottom")
        # self.show_bottom_card(pb_res)
    
    def show_gameover_board(self, winuser=None):
        if self.win == None:
            win = tk.Frame(self, width=500, height=300)
            # if winuser != None and winuser == self.username:
            #     win.wm_title("You win")
            # else:
            #     win.wm_title("You failed")
            # win.attributes('-alpha', 0.9)
            # win.resizable(0,0)
            # # win.attributes("-toolwindow", 1)
            # win.wm_attributes("-topmost", 1)
            # win.wm_overrideredirect(True)  
            # win.geometry("500x300")
            # win.minsize(500, 300)
            win.place(x=300, y=300)
            r = 0
            for place in self.places:
                l = tk.Label(win, text=self.places[place])
                l.grid(row=r, column=0)

                if winuser != None and winuser == self.places[place]:
                    l = tk.Label(win, text="Win")
                    l.grid(row=r, column=1)
                else:
                    l = tk.Label(win, text="Failed")
                    l.grid(row=r, column=1)
                r = r + 1

            r = r + 1
            r = r + 1
            r = r + 1
            r = r + 1
            b = tk.Button(win, text="返回房间", command=win.destroy)
            b.grid(row=r, column=0)

            def close():
                self.win.destroy()
                self.win=None
            # r = r + 1
            b = tk.Button(win, text="继续游戏", command=close)
            b.grid(row=r, column=1)
            self.win = win
        