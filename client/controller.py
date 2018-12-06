import tkinter.messagebox
import tkinter
from protocols import game_pb2
import struct
# from page import *
import page
from PIL import ImageTk, Image
from functools import partial

class Controller:
    def __init__(self, master):
        self.master = master

    def __getattr__(self, name):
        if not name in self.__dict__:
            return self.master.__dict__[name]
        return self.__dict__[name]


class LoginController(Controller):
    command = 0x0001
    def do_request(self, username, password):
        lr = game_pb2.LoginRequest()
        lr.username = username
        lr.password = password
        package = lr.SerializeToString()
        header_package = struct.pack(self.client.header_format, self.command, len(package))
        self.client.transport.write(header_package + package)
        self.master.username = username
        
    def on_response(self, pb_res):
        if pb_res.response.succ:
            self.master.switch_frame(page.PageHall)
            self.master.title(self.master.username)
        else:
            tkinter.messagebox.showwarning('提示', pb_res.response.mess)

class RegisterController(Controller):
    command = 0x0002
    def do_request(self, username, password):
        lr = game_pb2.RegisterRequest()
        lr.username = username
        lr.password = password
        package = lr.SerializeToString()
        header_package = struct.pack(self.client.header_format, self.command, len(package))
        self.client.transport.write(header_package + package)
        self.master.username = username

    def on_response(self, pb_res):
        if pb_res.response.succ:
            self.master.switch_frame(page.PageHall)
            self.master.title(self.master.username)
        else:
            tkinter.messagebox.showwarning('提示', pb_res.response.mess)

class HeartController(Controller):
    command = 0x0003
    def do_request(self):
        pass

    def on_response(self, pb_res):
        pass

class AddRoomController(Controller):
    command = 0x0005
    def do_request(self):
        pass

    def on_response(self, pb_res):
        pass

class RoomListController(Controller):
    command = 0x0004
    def do_request(self):
        lr = game_pb2.RoomListRequest()
        package = lr.SerializeToString()
        header_package = struct.pack(self.client.header_format, self.command, len(package))
        self.client.transport.write(header_package + package)

    def on_response(self, pb_res):
        frame = self.master._frame
        
        def redirect_room(e):
            self.master.entry_room_id = pb_res.room[e].id
            self.master.entry_room_name = pb_res.room[e].name
            self.master.switch_frame(page.PageRoom)
        
        paths = {}
        for i in range(0, len(pb_res.room)):
            file_path = page.down_for_url(pb_res.room[i].ico)
            im = Image.open(file_path)
            paths[i] = img = ImageTk.PhotoImage(im)

        for i in range(0, len(pb_res.room)):
            l = tkinter.Label(frame, image=paths[i])
            l.image=paths[i]
            b = tkinter.Button(frame, text=pb_res.room[i].name, command=partial(redirect_room, i))
            b.pack()
            l.pack()
        
        if self.master.client.default_username != None:
            redirect_room(0)

class EntryRoomController(Controller):
    command = 0x0007
    def do_request(self, id):
        lr = game_pb2.EntryRoomRequest()
        lr.id = id
        package = lr.SerializeToString()
        header_package = struct.pack(self.client.header_format, self.command, len(package))
        self.client.transport.write(header_package + package)

    def on_response(self, pb_res):
        if pb_res.response.succ:
            pass
        else:
            tkinter.messagebox.showwarning('提示', pb_res.response.mess)
            self.master.switch_frame(page.PageHall)

class LeaveRoomController(Controller):
    command = 0x0008
    def do_request(self):
        lr = game_pb2.LeaveRoomRequest()
        package = lr.SerializeToString()
        header_package = struct.pack(self.client.header_format, self.command, len(package))
        self.client.transport.write(header_package + package)

    def on_response(self, pb_res):
        self.logger.debug("LeaveRoomController on_response")
        self.master.switch_frame(page.PageHall)

class GameChupaiController(Controller):
    command = 0x0006
    def do_request(self, card):
        lr = game_pb2.GameChupaiRequest()
        lr.card[:] = card
        package = lr.SerializeToString()
        header_package = struct.pack(self.client.header_format, self.command, len(package))
        self.client.transport.write(header_package + package)

    def on_response(self, pb_res):
        self.logger.debug(pb_res)
        if pb_res.response.succ:
            pass
        else:
            for btn in self.master._frame.change_card:
                self.master._frame.add_change(btn.card_id)
            tkinter.messagebox.showwarning('提示', pb_res.response.mess)

class GameStartNotify(Controller):
    def on_response(self, pb_res):
        if isinstance(self.master._frame, page.PageRoom):
            self.master.switch_frame(page.PageGameDDZ)
            self.master._frame.init(pb_res)

class GameQueueNotify(Controller):
    def on_response(self, pb_res):
        if isinstance(self.master._frame, page.PageRoom):
            self.master._frame.tips["text"] = "当前排队人数:" + str(pb_res.entry_num)

class GameOverNotify(Controller):
    def on_response(self, pb_res):
        if isinstance(self.master._frame, page.PageGameDDZ):
            self.master._frame.show_gameover_board(pb_res.win)
            self.master._frame.append_show_center_card(pb_res.card)
            if pb_res.win == pb_res.username:
                if len(pb_res.card) > 0:
                    # self.master.logger.debug("bottom_card_num: {0}".format(self.master._frame.bottom_card_num))

                    a = list(self.master._frame.bottom_card_num).copy()
                    self.master._frame.change_card = []
                    for c in pb_res.card:
                        if c in a:
                            a.remove(c)

                    self.master._frame.bottom_card_num = a
                    self.master._frame.refresh_zddz_after_card("bottom")
                    
                    # 停止倒计时
                    self.master._frame.stop_caipai_count_down("bottom")
                # 移除按钮
                self.master._frame.remove_btns()
            else:
                for place in self.master._frame.places:
                    if self.master._frame.places[place] == pb_res.win:
                        if place == 'left':
                            self.master._frame.left_card_num = self.master._frame.left_card_num - len(pb_res.card)
                        if place == 'right':
                            self.master._frame.right_card_num = self.master._frame.right_card_num - len(pb_res.card)
                        self.master._frame.refresh_zddz_after_card(place)
                        self.master._frame.stop_caipai_count_down(place)

class GameFapaiNotify(Controller):
    def on_response(self, pb_res):
        pass

class GameChupaiNotify(Controller):
    def on_response(self, pb_res):
        if isinstance(self.master._frame, page.PageGameDDZ):
            if pb_res.chupai == pb_res.username:
                if len(pb_res.card) > 0:
                    self.master.logger.debug("bottom_card_num: {0}".format(self.master._frame.bottom_card_num))

                    a = list(self.master._frame.bottom_card_num).copy()
                    self.master._frame.change_card = []
                    for c in pb_res.card:
                        if c in a:
                            a.remove(c)

                    self.master._frame.bottom_card_num = a
                    self.master._frame.refresh_zddz_after_card("bottom")
                    
                    # 停止倒计时
                    self.master._frame.stop_caipai_count_down("bottom")
                # 移除按钮
                self.master._frame.remove_btns()
            else:
                for place in self.master._frame.places:
                    if self.master._frame.places[place] == pb_res.chupai:
                        if place == 'left':
                            self.master._frame.left_card_num = self.master._frame.left_card_num - len(pb_res.card)
                        if place == 'right':
                            self.master._frame.right_card_num = self.master._frame.right_card_num - len(pb_res.card)
                        self.master._frame.refresh_zddz_after_card(place)

            if pb_res.next == pb_res.username:
                self.master._frame.init_btns()

            # 显示下一家倒计时
            for place in self.master._frame.places:
                    if self.master._frame.places[place] == pb_res.next:
                        self.master._frame.show_caipai_count_down(place, pb_res.timeout)

            self.master.logger.debug("card {0}".format(pb_res.card))
            if len(pb_res.card) > 0:
                self.master._frame.append_show_center_card(pb_res.card)

class GameZddzController(Controller):
    command = 0x0009
    def do_request(self, z = False):
        lr = game_pb2.GameZddzRequest()
        lr.z = z
        package = lr.SerializeToString()
        header_package = struct.pack(self.client.header_format, self.command, len(package))
        self.client.transport.write(header_package + package)

    def on_response(self, pb_res):
        if isinstance(self.master._frame, page.PageGameDDZ):
            if pb_res.response.succ:
                pass
                # for btn in self.master._frame.bottom_zddz_btns:
                #     btn.destroy()
            else:
                tkinter.messagebox.showwarning('提示', pb_res.response.mess)

class GameZddzNotify(Controller):
    def on_response(self, pb_res):
        # self.logger.debug("收到抢地主通知: {0}".format(pb_res))
        if isinstance(self.master._frame, page.PageGameDDZ):
            if pb_res.action == pb_res.CONTINUE:
                self.master._frame.zddz_clear()
                for place in self.master._frame.places:
                    # 跳转下一个抢地主
                    if self.master._frame.places[place] == pb_res.value:
                        self.master._frame.zddz(place)
                        break

            if pb_res.action == pb_res.END_CHUPAI:
                self.master._frame.zddz_clear()
                for place in self.master._frame.places:
                    # 抢地主回合完成
                    if self.master._frame.places[place] == pb_res.value:
                        # 增加地主标识
                        if place == "left":
                            self.master._frame.left_username["text"] = "【地主】" + self.master._frame.left_username["text"]
                            self.master._frame.remove_btns()
                        elif place == "right":
                            self.master._frame.right_username["text"] = "【地主】" + self.master._frame.right_username["text"]
                            self.master._frame.remove_btns()
                        elif place == "bottom":
                            self.master._frame.bottom_username["text"] = "【地主】" + self.master._frame.bottom_username["text"]
                            self.master._frame.init_btns()

                        # 显示底牌
                        self.master._frame.show_card_bt(pb_res.card)
                        if place == "left":
                            self.master._frame.left_card_num = self.master._frame.left_card_num + len(pb_res.card)
                        if place == "right":
                            self.master._frame.right_card_num = self.master._frame.right_card_num + len(pb_res.card)
                        else:
                            self.master._frame.bottom_card_num.extend(pb_res.card)
                        self.master._frame.refresh_zddz_after_card(place)
                        self.master._frame.show_caipai_count_down(place, pb_res.timeout)
                        break
                

            if pb_res.action == pb_res.END_RE_XAIPAI:
                self.master._frame.zddz_clear()
                # 清空底牌
                self.master._frame.card_bt_clear()
                for place in self.master._frame.places:
                    if self.master._frame.places[place] == pb_res.value:
                        self.master._frame.zddz(place)
                        # self.master._frame.remove_bottom_card()
                        self.master._frame.bottom_card_num = pb_res.card
                        self.master._frame.show_bottom_card()
                        break

Executor = {
    0x0001: LoginController,
    0x0002: RegisterController,
    0x0003: HeartController,
    0x0004: RoomListController,
    0x0005: AddRoomController,
    0x0006: GameChupaiController,
    0x0007: EntryRoomController,
    0x0008: LeaveRoomController,
    0x0009: GameZddzController,
}

Notification = {
    0x1001: GameStartNotify,
    0x1002: GameQueueNotify,
    0x1003: GameOverNotify,
    0x1004: GameFapaiNotify,
    0x1005: GameChupaiNotify,
    0x1006: GameZddzNotify,
}