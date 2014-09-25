from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import struct

class NapsterProtocol(Protocol):

    def __init__(self):
        self.stage = 0
        self.buffer = ''

    def connectionMade(self):
        self.stage = 1

    def dataReceived(self, data):
        self.buffer += data
        if self.stage < 2:
            if len(self.buffer) > 512:
                #Attack or incorrnct protocl
                self.transport.abortConnection()
        else:
            if len(self.buffer) > 1024:
                #Send reason
                self.transport.loseConnection()

        type, data = self.messageParse()
        if type is None:
            return
        if type == 2:
            arr_str = data.split()
            print arr_str


    def messageParse(self):
        #<length><type><data>
        bufferlen = len(self.buffer)
        if bufferlen < 4:
            return None, None
        length = struct.unpack('<H', buffer[:2])
        if bufferlen > length + 4:
            type = struct.unpack('<H', buffer[2:4])
            data = bufferlen[4:length + 4]
            self.buffer = self.buffer[length + 4:]
            return type, data
        else:
            return False

class NapsterFactory(Factory):

    protocol = NapsterProtocol

    def __init__(self):
        protocol = NapsterProtocol
        self.user = {}

reactor.listenTCP(8888, NapsterFactory())
reactor.run()