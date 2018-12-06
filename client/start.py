# Multi-frame tkinter application v2.3
import tkinter as tk
import time
import arrow
# import asyncio
# import threading

import asyncio
import uvloop
import sys, os
import struct
import logging
# sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

from protocols import game_pb2
from controller import Executor, Notification
from page import *

class SimpleClientProtocol(asyncio.Protocol):

    def __init__(self, loop, queue, executor, logger, notification, default_username = None):
        if default_username:
            logger.basicConfig(level=logging.DEBUG,
                        format='{asctime} {levelname} {message} ' + default_username + ' ',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        style='{')
        self.loop = loop
        self.extra = bytearray()
        self.header_format = 'II'
        self.header_length = struct.calcsize(self.header_format)
        self.executor = executor
        self.command = 0x00001
        self.logger = logger
        self.queue = queue
        self.gui = SampleApp()
        self.gui.client = self
        self.gui.logger = logger
        self.notification = notification
        self.username = None
        self.default_username = default_username

    async def go_gui(self, interval=0.05):
        while True:
            self.gui.update()
            await asyncio.sleep(interval)

    def send(self, username, password):
        lr = game_pb2.LoginRequest()
        lr.username = "liuweilong"
        lr.password = "a123456"
        lr.username = username
        lr.password = password
        package = lr.SerializeToString()
        header_package = struct.pack(self.header_format, self.command, len(package))
        self.transport.write(header_package + package)

    def connection_made(self, transport):
        self.transport = transport
        asyncio.ensure_future(self.go_gui())

    def data_received(self, data):
        # self.logger.debug("received data: {0}".format(data))
        self.extra.extend(data)
        while True:
            try:
                command, body_length = struct.unpack(self.header_format, self.extra[:self.header_length])
                package_length = body_length + self.header_length
                if package_length <= len(self.extra):
                    data = self.extra[self.header_length:package_length]
                    asyncio.ensure_future(self.handle(command, data))
                    del self.extra[:package_length]
                else:
                    self.logger.debug("解包失败: {0} == {1} {2} {3}".format(package_length, len(self.extra), len(data), command))
                    break
            except Exception as e:
                # self.logger.debug("解包失败: {0}".format(e))
                break

    async def handle(self, command, data):
        self.logger.debug("handle: %x" % command)
        if command in self.executor:
            name = self.executor[command].__name__.replace("Controller", "")
            pb_res = getattr(game_pb2, name + "Response")()
            pb_res.ParseFromString(data)
            obj = self.executor[command](self.gui)
            obj.on_response(pb_res)
        
        if command in self.notification:
            # print("notify")
            name = self.notification[command].__name__.replace("Controller", "")
            pb_res = getattr(game_pb2, name)()
            pb_res.ParseFromString(data)
            obj = self.notification[command](self.gui)
            obj.on_response(pb_res)

    def connection_lost(self, exc):
        self.loop.stop()

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)
        self.title("Sample App")
        self.minsize(1024, 800)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


# async def do_gui(root, interval=0.05):
#     while True:
#         root.update()
#         await asyncio.sleep(interval)

# async def queue_task(queue):
#     while True:
#         item = await queue.get()
#         print(item)

if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    logging.basicConfig(level=logging.DEBUG,
                        format='{asctime} {levelname} {message}',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        style='{')

    loop = asyncio.get_event_loop()
    # queue = asyncio.Queue()
    # asyncio.Task(queue_task(queue))
    # app = SampleApp()
    # app.queue = queue
    try:
        default_username = sys.argv[1]
    except:
        default_username = None

    coro = loop.create_connection(lambda: SimpleClientProtocol(loop, 1, Executor, logging, Notification, default_username),
                                '127.0.0.1', 10086)
    loop.run_until_complete(coro)
    # loop.run_until_complete(do_gui(app))
    
    loop.run_forever()
    loop.close()
    
    