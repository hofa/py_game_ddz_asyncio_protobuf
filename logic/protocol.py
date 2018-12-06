import asyncio
import struct
from protocols import game_pb2
from logic import task


class ServerProtocol(asyncio.Protocol):

    def __init__(self, mongo, redis, clients, rooms, logger, executor, loop, nodes):
        self.mongo = mongo
        self.redis = redis
        self.clients = clients
        self.logger = logger
        self.executor = executor
        self.header_format = 'II'
        self.header_length = struct.calcsize(self.header_format)
        self.extra = bytearray()
        self.timeout = 500
        self.rooms = rooms
        self.current_room_id = None
        self.current_room_node_id = None
        self.loop = loop
        self.username = None
        self.is_login = False
        self.nodes = nodes

    def connection_made(self, transport):
        self.transport = transport
        self.peername = transport.get_extra_info("peername")
        self.logger.debug("connection_made: {}".format(self.peername))
        self.clients.append(self)

    def data_received(self, data):
        self.extra.extend(data)
        while True:
            try:
                command, body_length = struct.unpack(self.header_format, self.extra[:self.header_length])
                package_length = body_length + self.header_length
                self.logger.debug("package_length:{0} extra_length:{1}".format(package_length, len(self.extra)))
                if package_length <= len(self.extra):
                    data = self.extra[self.header_length:package_length]
                    asyncio.ensure_future(self.handle(command, data))
                    del self.extra[:package_length]
                else:
                    break
            except:
                break

    async def handle(self, command, data):
        if not command in self.executor:
            self.transport.lost_connection()
        
        self.logger.debug("command {0}".format(self.executor[command].__name__))
        name = self.executor[command].__name__
        pb_req = getattr(game_pb2, name + "Request")()
        pb_req.ParseFromString(data)
        exe = self.executor[command]()
        exe.set_context(self)
        pb_res = await exe.on_request(pb_req)
        res = pb_res.SerializeToString()  
        header_package = struct.pack(self.header_format, command, len(res))
        self.transport.write(header_package + res)
        
    def connection_lost(self, ex):
        self.logger.debug("connection_lost: {}".format(self.peername))
        self.clients.remove(self)
        try:
            self.rooms[self.current_room_id].remove(self)
        except:
            pass

    