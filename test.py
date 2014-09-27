import socket
import Message
import struct
import re

import time
import random

def rnd_data(n):
    data = ''
    while len(data) < n:
        temp = chr(random.randint(0,255))
        data = data.join(['', temp])
    return data

l = []
start = time.clock()
s = 'sdsfsddsfgtxdewtxt'
for i in range(0,100000):
    l.append(rnd_data(20))
d = []
end = time.clock()
print end-start

start = time.clock()
for i in l:
    if i.find('txt'):
        d = d
#run code
end = time.clock()
print end-start

address = ('127.0.0.1', 8888)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)

def message(msg_type, msg_data):
    if type(msg_data) is str:
        msg_data = msg_data
    else:
        msg_data = ' '.join(str(i) for i in msg_data)
    msg_len = struct.pack('<H', len(msg_data))
    msg_type = struct.pack('<H', msg_type)
    return msg_len + msg_type + msg_data

def messageParse(buff):
    #<length><type><data>
    bufflen = len(buff)
    if bufflen <= 4:
        return None, None
    length = struct.unpack('<H', buff[:2])[0]
    if bufflen >= length + 4:
        msg_type = struct.unpack('<H', buff[2:4])[0]
        msg_data = buff[4:length + 4]
        msg_data = re.findall(r'([^"^\s]+|"[\S ]+")', msg_data)
        buff = buff[length + 4:]
        print msg_type
        print msg_data
        return msg_type, msg_data
    else:
        return None, None
s.send(message(400, 'ch0'))

data = s.recv(1024)
messageParse(data)
print 'the data received is', data

s.send('hihi')
s.close()