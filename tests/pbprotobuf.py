import struct
from proto import sb_pb2
from EchoServer import reactor
class PbProtocol(protocol.Protocol, policies.TimeoutMixin):
    BUFFER = ''
    timeOut = 500
    header_format = 'IH'
    header_length = struct.calcsize(header_format)
    def connectionMade(self):
        self.transport.setTcpKeepAlive(True)
        self.setTimeout(self.timeOut)
        peer = self.transport.getPeer()
        print('Connection made. host, port:', peer.host, peer.port)
 
    def dataReceived(self, data):
        self.resetTimeout()
        self.transport.pauseProducing()
        self.BUFFER += data
        buffer_length = len(self.BUFFER)
        _l = ''
        while (buffer_length >= self.header_length):
            len_pb_data, len_msg_name = struct.unpack(self.header_format, self.BUFFER[:self.header_length])#_bound.ParseFromString(self.BUFFER[:8])
            if len_msg_name:
                if len_msg_name > len(self.BUFFER[self.header_length:]):
                    print('not enough buffer for msg name, wait for new data coming ...   ')
                    break
                else:
                    msg_name = struct.unpack('%ds'% len_msg_name,  self.BUFFER[self.header_length:len_msg_name + self.header_length])[0]
                    _func = getattr(self.factory.service, '%s' % msg_name.lower(), None) 
                    _msg =  getattr(sb_pb2, msg_name, None)
                    if _func and _msg:
                        _request = getattr(sb_pb2, msg_name)()
                        if len_pb_data <= len(self.BUFFER[self.header_length + len_msg_name :]):
                            _request.ParseFromString(self.BUFFER[self.header_length + len_msg_name : self.header_length + len_msg_name + len_pb_data])
                            reactor.callLater(0, _func, self, _request) 
                            self.BUFFER = self.BUFFER[self.header_length + len_msg_name + len_pb_data:]
                            buffer_length = len(self.BUFFER) 
                            continue
                        else:   
                            print('not enough buffer for pb_data, waiting for new data coming ... ')
                            break
                    else:
                        print('no such message handler. detail:', _func, hasattr(sb_pb2, msg_name), repr(self.BUFFER))
                        if self.fromclient:
                            self.transport.loseConnection()
                        else:
                            self.BUFFER = ''
 
                        return
            else:
                print('Un-supported message, no msg_name. detail:', len_msg_name)
                if self.fromclient:
                    self.transport.loseConnection()
                else:
                    self.BUFFER = ''
                return
            
        self.transport.resumeProducing()
        
 
    def send(self, msg):
        if msg:
            pb_data = msg.SerializeToString()
            _header = struct.pack(self.header_format + '%ds'%len(msg.__class__.__name__), len(pb_data), len(msg.__class__.__name__), msg.__class__.__name__)
            self.transport.write(_header + pb_data)
