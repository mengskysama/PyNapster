#!/usr/bin/python
# -*- coding: utf-8 -*-


class File(object):
    #"<filename>" <md5> <size> <bitrate> <frequency> <length> <nick> <ip> <link-type> [weight]
    def __init__(self, filename, md5, size, bitrate, frequency, length, nick, link, weight):
        self.filename = filename
        self.md5 = md5
        self.size = size
        self.bitrate = bitrate
        self.frequency = frequency
        self.length = length
        self.nick = nick
        self.link = link
        self.weight = weight

    def __list__(self):
        return [self.filename, self.md5, self.size, self.bitrate,
                self.frequency, self.length, self.nick, self.link, self.weight]


class FileList(object):

    def __init__(self):
        self.lst = []

    def get_files_by_name_include(self, include, max = 2000):
        if type(include) is not str:
            return
        ret = []
        for i in self.lst:
            if i.filename.find(include) != -1:
                ret.append(i)
                if len(ret) > max:
                    break
        return ret