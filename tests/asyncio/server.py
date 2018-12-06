class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport
        self.word_title = '我们一起来背诵 <<荷叶杯·记得那年花下>>'
        self.word_list = ['记得那年花下', '深夜', '初识谢娘时', '水堂西面画帘垂', '携手暗相期',
                          '惆怅晓莺残月', '相别', '从此隔音尘', '如今俱是异乡人', '相见更无因']
        self.index = 0

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))
        try:
            message = self.find_next(data=data.decode())
            print('Send: {!r}'.format(message))
            self.transport.write(message.encode())
        except (IndexError,ValueError):
            message = input('input the message:')
            print('Send: {!r}'.format(message))
            self.transport.write(message.encode())

    def find_next(self, data):
        index = self.word_list.index(data)
        return self.word_list[index + 1]


loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance
coro = loop.create_server(EchoServerClientProtocol, '127.0.0.1', 8888)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()