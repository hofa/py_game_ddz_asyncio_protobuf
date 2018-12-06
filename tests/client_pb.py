import asyncio
import uvloop
import sys, os
import struct
import logging
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

from protocols import game_pb2
from logic.executor import Executor

class SimpleClientProtocol(asyncio.Protocol):

    def __init__(self, loop, executor, logger):
        self.loop = loop
        self.extra = bytearray()
        self.header_format = 'II'
        self.header_length = struct.calcsize(self.header_format)
        self.executor = executor
        self.command = 0x00001
        self.logger = logger

    def connection_made(self, transport):
        self.transport = transport
        lr = game_pb2.LoginRequest()
        lr.username = "liuweilong"
        lr.password = "a123456"
        package = lr.SerializeToString()
        header_package = struct.pack(self.header_format, self.command, len(package))
        self.transport.write(header_package + package)

    def data_received(self, data):
        print("data_received", data)
        self.extra.extend(data)
        try:
            command, body_length = struct.unpack(self.header_format, self.extra[:self.header_length])
            package_length = body_length + self.header_length
            self.logger.debug("package_length:{0} extra_length:{1}".format(package_length, len(self.extra)))
            if package_length == len(self.extra):
                data = self.extra[self.header_length:package_length]
                asyncio.ensure_future(self.handle(command, data))
                del self.extra[:package_length]
        except:
            pass

    async def handle(self, command, data):
        if not command in self.executor:
            self.transport.lost_connection()
        
        self.logger.debug("command {0}".format(self.executor[command].__name__))
        name = self.executor[command].__name__
        pb_res = getattr(game_pb2, name + "Response")()
        pb_res.ParseFromString(data)
        self.logger.debug(pb_res)
        self.loop.stop()

    def connection_lost(self, exc):
        self.loop.stop()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='{asctime} {levelname} {message}',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        style='{')
    loop = asyncio.get_event_loop()
    coro = loop.create_connection(lambda: SimpleClientProtocol(loop, Executor, logging),
                                '127.0.0.1', 10086)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()