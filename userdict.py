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
        return UserDict.users[nick].shared_files.lst

    @staticmethod
    def add_file_by_nick(nick, file):
        if nick not in UserDict.users:
            return
        UserDict.users[nick].shared_files.lst.append(file)

    @staticmethod
    def del_file_by_nick(nick, filename):
        if nick not in UserDict.users:
            return
        UserDict.users[nick].shared_files.del_files_by_filename(filename)

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
                myfile.write('%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' %
                             (user.nick, user.email, user.passwd, user.user_level,
                             user.status, user.ip, user.connecting_port,
                             user.data_port, user.shared, user.uploads, user.downloads,
                             user.link_type, user.client_info, user.total_uploads,
                             user.total_downloads))

    @staticmethod
    def load():
        UserDict.users = {}
        with open('store.dat', 'r') as myfile:
            while True:
                line = myfile.readline()
                if line is (None or ''):
                    break
                arr_user = line.split(' ')
                user = User()
                user.nick = arr_user[0]
                user.email = arr_user[1]
                user.passwd = arr_user[2]
                user.user_level = arr_user[3]
                user.total_uploads = arr_user[13]
                user.total_downloads = arr_user[14]
                UserDict.users[user.nick] = user


UserDict.create_user('mengsky', '123456', '123@qq.com', 'User')
UserDict.store()
UserDict.load()

