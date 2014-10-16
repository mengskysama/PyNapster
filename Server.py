#!/usr/bin/python
# -*- coding: utf-8 -*-
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import struct
import re

import Message

class NapsterProtocol(Protocol):

    def __init__(self):
        self.stage = 0
        self.buff = ''

    def connectionMade(self):
        self.stage = 1

    def dataReceived(self, data):
        self.buff += data
        #most servers will not accept commands of length longer than 2048 bytes
        #Utatane not ignore it
        if self.stage < 2:
            if len(self.buff) > 128:
                #Attack or incorrnct protocl
                self.transport.abortConnection()
        else:
            if len(self.buff) > 4096:
                #Send reason
                self.transport.loseConnection()

        while True:
            msg_type, msg_data = self.messageParse()
            if msg_type is None:
                return

            if msg_type == 2:
                #<nick> <password> <port> "<client-info>" <link-type> [ <num> ]
                Message.MessageProcess.login(self, msg_data)
            elif msg_type == 208:
                Message.MessageProcess.hotlist(self, msg_data)
            elif msg_type == 211:
                Message.MessageProcess.browse_a_users_files(self, msg_data)
            elif msg_type == 400:
                Message.MessageProcess.join_channel(self, msg_data)
            elif msg_type == 402:
                Message.MessageProcess.send_public_message(self, msg_data)
            elif msg_type == 603:
                Message.MessageProcess.whois_request(self, msg_data)
            elif msg_type == 617:
                Message.MessageProcess.list_channels(self, msg_data)
            elif msg_type == 751:
                Message.MessageProcess.ping_user(self, msg_data)
            elif msg_type == 870:
                Message.MessageProcess.add_files_by_directory(self, msg_data)
            else:
                print 'Unknow Type %s' % msg_type
                print 'Unknow Data %s' % msg_data


    def messageParse(self):
        #<length><type><data>
        bufflen = len(self.buff)
        if bufflen < 4:
            return None, None
        length = struct.unpack('<H', self.buff[:2])[0]
        if bufflen >= length + 4:
            msg_type = struct.unpack('<H', self.buff[2:4])[0]
            msg_data = self.buff[4:length + 4]
            msg_data = re.findall(r'([^"^\s]+|"[\S ]?")', msg_data)
            self.buff = self.buff[length + 4:]
            #print msg_type
            #print msg_data
            return msg_type, msg_data
        else:
            return None, None

class NapsterFactory(Factory):

    protocol = NapsterProtocol

    def __init__(self):
        protocol = NapsterProtocol
        self.user = {}

reactor.listenTCP(8888, NapsterFactory())
reactor.run()