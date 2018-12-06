from protocols import game_pb2
import struct
class Logic:
    def set_context(self, context):
        self.context = context

    def __getattr__(self, name):
        if not name in self.__dict__:
            return self.context.__dict__[name]
        return self.__dict__[name]

class Login(Logic):
    async def on_request(self, request):
        pb_res = game_pb2.LoginResponse()
        self.logger.debug(request.username)
        user_data = await self.mongo.user.find_one({"username": request.username})
        if user_data and user_data["password"] == request.password:
            self.logger.debug(user_data)
            with await self.redis as conn:
                await conn.execute("SETEX", "login_auth:" + request.username, 20 * 60, 1)
            pb_res.response.succ = True
            pb_res.response.code = 1
            pb_res.response.mess = "注册成功"
            self.context.username = request.username
            self.context.is_login = False
        else:
            pb_res.response.succ = False
            pb_res.response.code = 1
            pb_res.response.mess = "用户不存在或者密码错误！"
        return pb_res

class Register(Logic):
    async def on_request(self, request):
        self.logger.debug(request.username)
        user_data = await self.mongo.user.find_one({"username": request.username})
        pb_res = game_pb2.RegisterResponse()
        if user_data:
            self.logger.debug(user_data)
            pb_res.response.succ = False
            pb_res.response.code = 1
            pb_res.response.mess = "玩家已存在"
        else:
            res = await self.mongo.user.insert_one({"username": request.username, "password": request.password})
            pb_res.response.succ = True
            pb_res.response.code = 1
            pb_res.response.mess = "注册成功"

            with await self.redis as conn:
                await conn.execute("SETEX", "login_auth:" + request.username, 20 * 60, 1)
            
            self.context.username = request.username
            self.context.is_login = False
          
        return pb_res

class Heart(Logic):
    async def on_request(self, request):
        pb_res = game_pb2.HeartResponse()
        with await self.redis as conn:
            res = await conn.execute("get", "login_auth:" + request.username, 20 * 60, 1)
            if res != 1:
                pb_res.response.succ = False
                pb_res.response.code = 1
                pb_res.response.mess = "登录超时"

        with await self.redis as conn:
            await conn.execute("SETEX", "login_auth:" + request.username, 20 * 60, 1)
            pb_res.response.succ = True
            pb_res.response.code = 1
            pb_res.response.mess = "续期成功"
        
class RoomList(Logic):
    async def on_request(self, request):
        pb_res = game_pb2.RoomListResponse()
        pb_res.response.succ = True
        pb_res.response.code = 1
        pb_res.response.mess = ""

        data = [
            {
                "id": "sb1",
                "ico": "http://t1.27270.com/uploads/tu/MN/533/wlmn.jpg",
                "name": "房间1",
            },
            {
                "id": "sb2",
                "ico": "http://t1.27270.com/uploads/tu/MN/532/twmn.jpg",
                "name": "房间2",
            },
            {
                "id": "sb3",
                "ico": "http://t1.27270.com/uploads/tu/MN/532/zgmn.jpg",
                "name": "房间3",
            },
        ]
        for d in data:
            a = pb_res.room.add()
            a.id = d["id"]
            a.ico = d["ico"]
            a.name = d["name"]
        return pb_res

class AddRoom(Logic):
    async def on_request(self, request):
        pass

class EntryRoom(Logic):
    async def on_request(self, request):
        pb_res = game_pb2.EntryRoomResponse()
        if self.context.current_room_node_id == None:

            if request.id in self.rooms and self.context not in self.rooms[request.id]:
                self.context.current_room_id = request.id
                self.rooms[self.current_room_id].append(self.context)
            else:
                pass
            pb_res.response.succ = True
        else:
            pb_res.response.succ = False
            pb_res.response.mess = "游戏锁定中"
        
        return pb_res

class LeaveRoom(Logic):
    async def on_request(self, request):
        pb_res = game_pb2.LeaveRoomResponse()
        if self.context.current_room_node_id == None:
            try:
                self.rooms[self.current_room_id].remove(self.context)
            except:
                pass
            pb_res.response.succ = True
        else:
            pb_res.response.succ = False
            pb_res.response.mess = "游戏锁定中"
        return pb_res

class GameZddz(Logic):

    def do_notify(self, ddz, clients, action, value):
        notify = game_pb2.GameZddzNotify()
        notify.response.succ = True
        notify.zddz_username = ''
        if action == 'continue':
            notify.action = notify.CONTINUE
            value = ddz.usernames[value]

        if action == 'end_chupai':
            notify.action = notify.END_CHUPAI
            notify.card[:] = ddz.get_card_bt()
            value = ddz.usernames[value]
            
        if action == 'end_re_xaipai':
            notify.action = notify.END_RE_XAIPAI
            value = ddz.usernames[value]

        notify.value = str(value)
        notify.timeout = 30

        if action != 'end_re_xaipai':
            notify.z = ddz.current_zddz_z
            notify.zddz_username = ddz.get_play_name(ddz.current_zddz_index)

        for client in clients:
            if action == 'end_re_xaipai':
                play_index = ddz.get_play_index(client.username)
                notify.card[:] = ddz.get_play_card(play_index)

            notify.username = client.username
            package = notify.SerializeToString()
            header_package = struct.pack(self.header_format, 0x1006, len(package))
            client.transport.write(header_package + package)
        
        # self.logger.debug("抢地主通知: action={0} {1}".format(action, notify))

    async def on_request(self, request):
        pb_res = game_pb2.LeaveRoomResponse()
        if self.current_room_node_id:
            if self.current_room_node_id in self.nodes:
                ddz = self.nodes[self.current_room_node_id]["DDZ"]
                action, value, errmessage = ddz.do_zddz(self.username, request.z)
                if action == 'fail':
                    pb_res.response.succ = False
                    pb_res.response.mess = str(errmessage)
                else:
                    pb_res.response.succ = True
                    # pb_res.response.mess = str(errmessage)
                self.do_notify(ddz, self.nodes[self.current_room_node_id]["clients"], action, value)
            else:
                pb_res.response.succ = False
                pb_res.response.mess = "比赛不存在"
        else:
            pb_res.response.succ = False
            pb_res.response.mess = "比赛还没有开始"
        
        return pb_res

class GameChupai(Logic):

    def do_notify(self, ddz, clients):
        over, win_index = ddz.check_game_over()
        if over:
            notify = game_pb2.GameOverNotify()
            notify.card[:] = ddz.current_chupai_card
            notify.win = ddz.get_play_name(win_index) 
            for client in clients:
                notify.username = client.username
                package = notify.SerializeToString()
                header_package = struct.pack(self.header_format, 0x1003, len(package))
                client.transport.write(header_package + package)
        else:
            notify = game_pb2.GameChupaiNotify()
            notify.chupai = ddz.get_play_name(ddz.current_chupai_index)
            notify.card[:] = ddz.current_chupai_card
            notify.timeout = 30
            res = ddz.get_current_ready_chupai_play_index()
            notify.next = ddz.get_play_name(res[0])
            for client in clients:
                notify.username = client.username
                package = notify.SerializeToString()
                header_package = struct.pack(self.header_format, 0x1005, len(package))
                client.transport.write(header_package + package)

    async def on_request(self, request):
        pb_res = game_pb2.GameChupaiResponse()
        pb_res.response.succ = False
        pb_res.response.mess = "奇怪的错误"
        if self.current_room_node_id != None and self.current_room_node_id in self.nodes:
            ddz = self.nodes[self.current_room_node_id]["DDZ"]
            self.logger.debug("GameChupai card: {0}".format(request.card))
            allow, message = ddz.do_chupai(self.username, request.card)
            self.logger.debug("GameChupai {0} {1}".format(allow, message))
            if allow:
                pb_res.response.succ = True
                self.do_notify(ddz, self.nodes[self.current_room_node_id]["clients"])
            else:
                pb_res.response.succ = False
                pb_res.response.mess = message
        else:
            pb_res.response.succ = False
            pb_res.response.mess = "房间已经解散"
        return pb_res

Executor = {
    0x0001: Login,
    0x0002: Register,
    0x0003: Heart,
    0x0004: RoomList,
    0x0005: AddRoom,
    0x0006: GameChupai,
    0x0007: EntryRoom,
    0x0008: LeaveRoom,
    0x0009: GameZddz,
}

Notification = {
    0x1001: game_pb2.GameStartNotify,
    0x1002: game_pb2.GameQueueNotify,
    0x1003: game_pb2.GameOverNotify,
    0x1004: game_pb2.GameFapaiNotify,
    0x1005: game_pb2.GameChupaiNotify,
    0x1006: game_pb2.GameZddzNotify,
}