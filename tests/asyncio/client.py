class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop
        self.transport = None
        self.word_title = '我们一起来背诵 <<荷叶杯·记得那年花下>>'
        self.word_list = ['记得那年花下', '深夜', '初识谢娘时', '水堂西面画帘垂', '携手暗相期',
                          '惆怅晓莺残月', '相别', '从此隔音尘', '如今俱是异乡人', '相见更无因']
        self.index = 0
        print(self.word_title)

    def connection_made(self, transport):
        self.transport = transport
        message = self.word_list[self.index]
        print('message: ',message)
        self.transport.write(message.encode())

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))
        try:
           message = self.find_next(data=data.decode())
           self.transport.write(message.encode())
           print('Data sent: {!r}'.format(message))
        except (IndexError,ValueError):
            message = input('input message:')
            self.transport.write(message.encode())
            print('Data sent: {!r}'.format(message))



    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

    def find_next(self, data):
        index = self.word_list.index(data)
        return self.word_list[index + 1]


loop = asyncio.get_event_loop()
coro = loop.create_connection(lambda: EchoClientProtocol(loop),
                              '127.0.0.1', 8888)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()