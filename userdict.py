#!/usr/bin/python
# -*- coding: utf-8 -*-
import filelist


class User(object):

    def __init__(self):
        self.nick               = None
        self.email              = None
        self.passwd             = None
        self.user_level         = 'User'
        self.channels           = []
        self.status             = 'Inactive'
        self.ip                 = 0
        self.connecting_port    = 0
        self.data_port          = 0
        self.shared             = 0
        self.uploads            = 0
        self.downloads          = 0
        self.link_type          = 0
        self.client_info        = ''
        self.total_uploads      = 0
        self.total_downloads    = 0
        self.shared_files       = filelist.FileList()


class UserDict(object):

    users = {}

    @staticmethod
    def get_user_by_nick(nick):
        if nick not in UserDict.users:
            return None
        return UserDict[nick]

    @staticmethod
    def create_user(self, nick, passwd, email, user_level):
        if nick in UserDict.users:
            return False
        user = User()
        user.nick = nick
        user.passwd = passwd
        user.email = email
        user.user_level = user_level
        UserDict.users[nick] = user
        return True

    @staticmethod
    def store():

