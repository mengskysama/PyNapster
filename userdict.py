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
    def get_files_by_nick(nick):
        if nick not in UserDict.users:
            return []
        return list(UserDict.users[nick].shared_files)

    @staticmethod
    def create_user(nick, passwd, email, user_level):
        if nick in UserDict.users:
            return False
        user = User()
        user.nick = nick
        user.passwd = passwd
        user.email = email
        user.user_level = user_level
        UserDict.users[nick] = user
        return True

    #@staticmethod
    #def store():
    #    with open('store.dat', 'wb') as myfile:
    #        pickle.dump(UserDict.users, myfile)

    @staticmethod
    def store():
        with open('store.dat', 'w') as myfile:
            for key in UserDict.users.keys():
                user = UserDict.users[key]
                myfile.write('%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' %
                             (user.nick, user.email, user.passwd, user.user_level,
                             user.channels, user.status, user.ip, user.connecting_port,
                             user.data_port, user.shared, user.uploads, user.downloads,
                             user.link_type, user.client_info, user.total_uploads,
                             user.total_downloads))

    @staticmethod
    def load():
        with open('store.dat', 'r') as myfile:
            while True:
                line = myfile.readline()
                if line is (None or ''):
                    break
                print line.split(' ')
                

UserDict.create_user('mengsky', '123456', '123@qq.com', 'User')
UserDict.store()
UserDict.load()

