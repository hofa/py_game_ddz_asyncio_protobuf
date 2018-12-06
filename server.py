import asyncio
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
from logic.protocol import ServerProtocol
from logic.executor import Executor
from logic import task
from motor.motor_asyncio import AsyncIOMotorClient
import logging
import aioredis

async def connect():
    return await aioredis.create_pool(address=(str('192.168.10.57'), int(6379)),
                                                                    password='123456', 
                                                                    db=0, 
                                                                    encoding='utf-8',
                                                                    minsize=1, maxsize=10, loop=loop)
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                    format='{asctime} {levelname} {message}',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    style='{')

    monogo = AsyncIOMotorClient('mongodb://192.168.10.57:27017')["foo"]

    clients = []
    rooms = {"sb1": [], "sb2":[], "sb3": []}
    nodes = {}
    loop = asyncio.get_event_loop()
    redis = loop.run_until_complete(connect())
    coro = loop.create_server(lambda: ServerProtocol(mongo=monogo, redis=redis, clients=clients, rooms=rooms, logger=logging, executor=Executor, loop=loop, nodes=nodes), port=10086)
    server = loop.run_until_complete(coro)
    for socket in server.sockets:
       print("serving on {}".format(socket.getsockname()))

    # 启用房间定时器
    for room_id in rooms:
        asyncio.ensure_future(task.room_task(room_id, rooms, logging, nodes))
    loop.run_forever()