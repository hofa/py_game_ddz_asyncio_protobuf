import asyncio
import sys
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
from motor.motor_asyncio import AsyncIOMotorClient

clients = []
class SimpleChatClientProtocol(asyncio.Protocol):

    # def __init__(self, db, redis):
    #     self.db = db
    #     self.redis = redis

    def connection_made(self, transport):
        self.transport = transport
        self.peername = transport.get_extra_info("peername")
        print("connection_made: {}".format(self.peername))
        clients.append(self)

    def data_received(self, data):
        # print("data_received: {}".format(data.decode()))
        # self.transport.write(data)
        # for client in clients:
        #     if client is not self:
        #         client.transport.write("{}: {}".format(self.peername, data.decode()).encode())
        # await handle(self.transport, data)
        res = asyncio.ensure_future(self.handle(data))
        print("on_request", res)

    async def handle(self, data):
        res = await self.on_request(data)
        await self.on_response(res)

    async def on_response(self, data):
        self.transport.write(bytes(data))

    async def on_request(self, data):
        await asyncio.sleep(1)
        return 1

    def connection_lost(self, ex):
        print("connection_lost: {}".format(self.peername))
        clients.remove(self)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # sb = 99
    # db = AsyncIOMotorClient('mongodb://192.168.1.57:27017')["foo"]
    coro = loop.create_server(lambda: SimpleChatClientProtocol(), port=10086)
    server = loop.run_until_complete(coro)
    for socket in server.sockets:
       print("serving on {}".format(socket.getsockname()))
    loop.run_forever()