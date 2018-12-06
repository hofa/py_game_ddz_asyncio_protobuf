import asyncio
from protocols import game_pb2
import struct
import random
from logic import ddz
import arrow
from logic import executor
header_format = 'II'
async def room_task(room_id, rooms, logger, nodes):
    oldNum = 0
    notify_command = 0x1002
    game_start_command = 0x1001
    while True:
        num = len(rooms[room_id])
        if num:
            # self.logger.debug("房间: {0} 人数: {1}".format(self.rooms[room_id], num))
            if oldNum != num:
                logger.debug("rooms: {0} {1} {2}".format(oldNum, num, room_id))
                oldNum = num
                notify = game_pb2.GameQueueNotify()
                notify.entry_num = len(rooms[room_id])

                # 发起通知
                package = notify.SerializeToString()  
                header_package = struct.pack(header_format, notify_command, len(package))
                for client in rooms[room_id]:
                    logger.debug("notify online num")
                    client.transport.write(header_package + package)

        if num >= 3:
            logger.debug("start node: %d" % num)
            node_id = None
            while True:
                unique_id = ''.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 5))
                node_id = room_id + '-' + unique_id
                if node_id not in nodes:
                    nodes[node_id] = {"clients": [], "DDZ": None}
                    # 将玩家加入节点
                    nodes[node_id]["clients"] = rooms[room_id][0:3]
                    break

            notify = game_pb2.GameStartNotify()
            usernames = []
            for room in rooms[room_id][0:3]:
                usernames.append(room.username)

            nodes[node_id]["DDZ"] = ddz.DouDiZhu(usernames, logger)
            nodes[node_id]["DDZ"].do_xipai().do_fapai().do_sortcard()
            for i in nodes[node_id]["DDZ"].get_play_card():
                add = notify.player.add()
                add.username = usernames[i]
                add.card_num = len(nodes[node_id]["DDZ"].get_play_card(i))

            # first = random.choice(usernames)
            # 设定谁先开始抢地主
            # nodes[node_id]["DDZ"].first = usernames.index(first)
            # 发起游戏开始通知
            notify.room_id = room_id
            notify.node_id = node_id

            # 设定谁先开始
            notify.first = usernames[nodes[node_id]["DDZ"].get_random_zddz_start()]
            logger.debug("usernames: {0}".format(usernames))
            # 三张底牌
            # notify.bcard.extend(nodes[node_id]["DDZ"].card_bt)

            for client in rooms[room_id][0:3]:
                client.current_room_node_id = node_id
                notify.username = client.username
                index = usernames.index(client.username)
                # del notify.card
                logger.debug("user:{0} card:{1}".format(notify.username, nodes[node_id]["DDZ"].get_play_card(index)))
                notify.card[:] = nodes[node_id]["DDZ"].get_play_card(index)

                package = notify.SerializeToString()
                header_package = struct.pack(header_format, game_start_command, len(package))
                client.transport.write(header_package + package)

            del rooms[room_id][0:3]
            asyncio.ensure_future(room_node_task(room_id, rooms, node_id, nodes, logger))

        await asyncio.sleep(1)




async def room_node_task(room_id, rooms, node_id, nodes, logger):
    
    start_time = arrow.now()
    timeout = 54 * 60
    game_over_command = 0x1003
    notify = game_pb2.GameOverNotify()
    bout_timeout = 30
    bout_timeout = 0.1
    def zddz_callback_func(ddz, res):
        # logger.debug("超时任务触发 {0}".format(res))
        gz = executor.GameZddz()
        gz.logger = logger
        gz.nodes = nodes
        gz.header_format = header_format
        gz.do_notify(ddz, nodes[node_id]["clients"], res[0], res[1])

    def chupai_callback_func(ddz, res):
        # logger.debug("超时任务触发 {0}".format(res))
        allow, message = res
        if allow:
            gz = executor.GameChupai()
            gz.logger = logger
            gz.nodes = nodes
            gz.header_format = header_format
            # gz.do_notify(ddz, nodes[node_id]["clients"], res[0], res[1])
            gz.do_notify(ddz, nodes[node_id]["clients"])

    while True:
        if node_id in nodes:
            dz = nodes[node_id]["DDZ"]
            # 检查超时行为
            dz.do_timeout_auto_next(timeout=bout_timeout, zddz_callback=zddz_callback_func, chupai_callback=chupai_callback_func)
        else:
            break
            
        # 超时判断
        end_time = arrow.now()
        if end_time.timestamp - start_time.timestamp > timeout:
            for client in nodes[node_id]["clients"]:
                notify.response.succ = False
                notify.response.mess = "超时结束"
                package = notify.SerializeToString()
                header_package = struct.pack(header_format, game_over_command, len(package))
                client.transport.write(header_package + package)

            del nodes[node_id]
            break


        await asyncio.sleep(1)