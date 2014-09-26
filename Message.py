#!/usr/bin/python
# -*- coding: utf-8 -*-

import struct

class MessageProcess():

    def __init__(self):
        pass

    @staticmethod
    def send(handler, data):
        handler.transport.write(data)

    @staticmethod
    def send_message(handler, msg_type, msg_data):
        if type(msg_data) is list:
            msg_data = ' '.join(str(i) for i in msg_data)
        msg_len = struct.pack('<H', len(msg_data))
        msg_type = struct.pack('<H', msg_type)
        #print repr(msg_len + msg_type + msg_data)
        MessageProcess.send(handler, msg_len + msg_type + msg_data)

    @staticmethod
    def error_message(handler, data):
        MessageProcess.send_message(handler, 0, data)

    @staticmethod
    def login(handler, msg_data):
        #2
        #<nick> <password> <port> "<client-info>" <link-type> [ <num> ]
        if len(msg_data) < 5:
            MessageProcess.error_message(handler, 'protocol err')
        MessageProcess.login_ack(handler, 'mengskysama@gmail.com')
        handler.stage = 2
        MessageProcess.message_of_the_day_resp(handler, 'Welcom!')
        MessageProcess.server_stats_resp(handler, '123 1 1024')

    @staticmethod
    def login_ack(handler, msg_data):
        #3
        #<email>
        MessageProcess.send_message(handler, 3, msg_data)

    #4 version check [CLIENT]
    #5 "auto-upgrade" [SERVER]
    #6 new user login Utatane  not use
    #7 nick check [CLIENT] Utatane  not use
    #8 nickname not registered [SERVER] #7 Utatane not use
    #9 nickname already registered [SERVER] Utatane not use
    #10 invalid nickname [SERVER] Utatane not use
    #11 12 13 14 Utatane not use

    @staticmethod
    def client_notification_of_shared_file(handler, msg_data):
        #100
        #Utatane not use
        #"<filename>" <md5> <size> <bitrate> <frequency> <time>
        pass

    #102 (0x66)	remove file [CLIENT] Utatane not use
    #110		unshare all files [CLIENT] Utatane not use

    @staticmethod
    def client_search_request(handler, msg_data):
        #200 [FILENAME CONTAINS "artist name"] MAX_RESULTS <max> [FILENAME CONTAINS
        #"song"] [LINESPEED <compare> <link-type>] [BITRATE <compare> "<br>"] [FREQ
        #<compare> "<freq>"] [WMA-FILE] [LOCAL_ONLY]
        #Utatane
        #FILENAME CONTAINS "exe" BITRATE "EQUAL TO" "24" FREQ "EQUAL TO" "16000"
        #FILENAME CONTAINS "exe" ALL  MP3/ALL
        #FILENAME CONTAINS "exe" BITRATE "AT LEAST" "128"
        #FILENAME CONTAINS "exe" BITRATE "AT LEAST" "128" SIZE "AT BEST" 1024
        #FILENAME CONTAINS "exe" LINESPEED "AT LEAST" 5 BITRATE "AT LEAST" "128" SIZE "AT BEST" 1024
        #FILENAME CONTAINS "exe" LINESPEED "AT LEAST" 10 BITRATE "AT LEAST" "128" SIZE "EQUAL TO" 1024
        pass

    @staticmethod
    def private_message(handler, msg_data):
        #205
        #private message to/from another user [CLIENT, SERVER]
        #Utatane
        pass

    @staticmethod
    def hotlist(handler, msg_data):
        #208
        # #This message is used to send the initial list of hotlist entries
        #to the add file (100) commands.  To add more entries to the hotlist
        #after the initial list is sent, clients should use the 207 message
        #instead.
        #<user>
        MessageProcess.user_signon(handler, '10')

    @staticmethod
    def user_signon(handler, msg_data):
        #
        #server is notifying client that a user in their hotlist, <user>,
        #has signed on the server with link <speed>
        #<user> <speed>
        MessageProcess.send_message(handler, 209, msg_data)

    @staticmethod
    def browse_a_users_files(handler, msg_data):
        #211
        #the client sends this message when it wants to get a list of the files shared by a specific client
        #<nick>
        #发送文件信息
        MessageProcess.browse_response(handler, 'mengskysama "D:\\a.rar" '
                                                '00000000000000000000000000000000 1024 0 0 0')
        #发送结束
        #why ip ret 0?
        MessageProcess.end_of_browse_list(handler, 'mengskysama 0')

    @staticmethod
    def browse_response(handler, msg_data):
        #<nick> "<filename>" <md5> <size> <bitrate> <frequency> <time>
        MessageProcess.send_message(handler, 212, msg_data)

    @staticmethod
    def end_of_browse_list(handler, msg_data):
        #indicates no more entries in the browse list for <user>.  <ip> gives
        #the client's IP address.
        #<nick> [ip]
        MessageProcess.send_message(handler, 213, msg_data)

    @staticmethod
    def server_stats_resp(handler, msg_data):
        #<users> <# files> <size>
        #服务器 用户/文件/容量
        #登陆之后服务器会发这个 貌似是每分钟发一次
        MessageProcess.send_message(handler, 214, msg_data)

    @staticmethod
    def whois_request(handler, msg_data):
        #查询用户信息 自己的?

        MessageProcess.whois_response(handler, 'lefty "User" 1203 "80\'s " "Active" 0 0 0 10 "nap v0.8"')

    @staticmethod
    def whois_response(handler, msg_data):
        #查询用户信息 自己的?
        #<nick> "<user-level>" <time> "<channels>" "<status>" <shared>
        #<downloads> <uploads> <link-type> "<client-info>" [ <total downloads>
        #<total_uploads> <ip> <connecting port> <data port> <email> ]
        MessageProcess.send_message(handler, 604, msg_data)

    @staticmethod
    def join_channel(handler, msg_data):
        #400
        #加入频道
        #<channel-name>
        #success
        MessageProcess.join_acknowledge(handler, 'ch0')

    @staticmethod
    def send_public_message(handler, msg_data):
        #402
        #发送频道消息
        #<channel> <message>
        #广播
        msg_data.insert(1, 'mengskysama')
        MessageProcess.public_message(handler, msg_data)

    @staticmethod
    def public_message(handler, msg_data):
        #403
        #广播消息
        #<channel> <nick> <text>
        #广播消息
        MessageProcess.send_message(handler, 403, msg_data)


    @staticmethod
    def join_acknowledge(handler, msg_data):
        #加入频道服务器返回
        #<channel>
        MessageProcess.send_message(handler, 405, msg_data)

        #发送用户列表
        MessageProcess.channel_user_list_entry(handler, 'ch0 mengskysama0 1 10')
        MessageProcess.channel_user_list_entry(handler, 'ch0 mengskysama1 1 10')
        MessageProcess.channel_user_list_entry(handler, 'ch0 mengskysama2 1 10')
        MessageProcess.channel_user_list_entry(handler, 'ch0 mengskysama 1 10')
        #发送结束包
        MessageProcess.end_of_channel_user_list(handler, 'ch0')

        #发送Toptic
        MessageProcess.channel_topic(handler, 'ch0 OpenNap help channel0')
        #发送欢迎信息
        MessageProcess.emote(handler, 'ch0 Bot "Welcome CH0"')
        MessageProcess.emote(handler, 'ch0 Bot "Fork! go away"')

        #广播信息
        #MessageProcess.channel_user_list_entry(handler, '')

    @staticmethod
    def join_message(handler, msg_data):
        #频道用户信息
        #<channel> <user> <sharing> <link-type>
        MessageProcess.send_message(handler, 406, msg_data)

    @staticmethod
    def channel_user_list_entry(handler, msg_data):
        #频道用户信息
        #<channel> <user> <sharing> <link-type>
        MessageProcess.send_message(handler, 408, msg_data)

    @staticmethod
    def end_of_channel_user_list(handler, msg_data):
        #频道列表结束包
        #<channel>
        MessageProcess.send_message(handler, 409, msg_data)

    @staticmethod
    def channel_topic(handler, msg_data):
        #<channel> <topic>
        MessageProcess.send_message(handler, 410, msg_data)



    @staticmethod
    def message_of_the_day_req(handler, msg_data):
        #服务器信息
        MessageProcess.message_of_the_day_resp(handler, msg_data)

    @staticmethod
    def message_of_the_day_resp(handler, msg_data):
        #<text>
        #服务器信息
        MessageProcess.send_message(handler, 621, msg_data)

    @staticmethod
    def list_channels(handler, msg_data):
        #617 (0x269)	list channels [CLIENT, SERVER]
        #<channel> <number-of-users> <topic>
        #查询频道
        MessageProcess.channel_list_entry(handler, 'ch0 50 OpenNap help channel0')
        MessageProcess.channel_list_entry(handler, 'ch1 50 OpenNap help channel1')

    @staticmethod
    def channel_list_entry(handler, msg_data):
        #<channel-name> <number-of-users> <topic>
        MessageProcess.send_message(handler, 618, msg_data)



    @staticmethod
    def ping_user(handler, msg_data):
        #<user>
        MessageProcess.pong_response(handler, msg_data)

    @staticmethod
    def pong_response(handler, msg_data):
        #<user>
        MessageProcess.send_message(handler, 752, msg_data)

    @staticmethod
    def emote(handler, msg_data):
        # A variation of the public message command to indicate an action by the user.
        # Often implemented as the "/me" command in IRC clients.
        #client: <channel> "<text>"
        # #server: <channel> <user> "<text>"
        MessageProcess.send_message(handler, 824, msg_data)

    @staticmethod
    def add_files_by_directory(handler, msg_data):
        #870
        #"<directory>" "<file>" <md5> <size> <bitrate> <freq> <duration>
        #for i in msg_data:
        #    print i
        #MessageProcess.send_message(handler, 870, msg_data)
        pass