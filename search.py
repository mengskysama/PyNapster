#!/usr/bin/python
# -*- coding: utf-8 -*-

class Search(object):

    @staticmethod
    def asynSearch(msg_data):
        #FILENAME CONTAINS "exe" BITRATE "EQUAL TO" "24" FREQ "EQUAL TO" "16000"
        #FILENAME CONTAINS "exe"
        #FILENAME CONTAINS "exe" BITRATE "AT LEAST" "128"
        #FILENAME CONTAINS "exe" BITRATE "AT LEAST" "128" SIZE "AT BEST" 1024
        #FILENAME CONTAINS "exe" LINESPEED "AT LEAST" 5 BITRATE "AT LEAST" "128" SIZE "AT BEST" 1024
        #FILENAME CONTAINS "exe" LINESPEED "AT LEAST" 10 BITRATE "AT LEAST" "128" SIZE "EQUAL TO" 1024
        try:
            if len(msg_data) < 3:
                return
            key = msg_data[2][1:-1]
            #"<filename>" <md5> <size> <bitrate> <frequency> <length> <nick> <ip> <link-type> [weight]
            if len(msg_data) > 12:
                #hack?
                return
            if len(msg_data) > 3:
                msg_data = ' '.join(str(i) for i in msg_data[3:])
                msg_data = msg_data.replace('LINESPEED', 'AND LINESPEED')
                msg_data = msg_data.replace('BITRATE', 'AND BITRATE')
                msg_data = msg_data.replace('SIZE', 'AND BITRATE')
                msg_data = msg_data.replace('"AT LEAST"', '>=')
                msg_data = msg_data.replace('"AT LEAST"', '<=')
                msg_data = msg_data.replace('"EQUAL TO"', '=')
                sql = 'SELECT `PATH`,`FILENAME`,`MD5`,`SIZE`,`BITRATE`,`FREQUENCY`,`LENGTH` ' \
                           'FROM `file_table` WHERE `FILENAME` LIKE %'+ key + '% AND ' + msg_data
            elif len(msg_data) == 3:
                sql = 'SELECT `PATH`,`FILENAME`,`MD5`,`SIZE`,`BITRATE`,`FREQUENCY`,`LENGTH` ' \
                           'FROM `file_table` WHERE `FILENAME` LIKE %'+ key + '%'
            #exec
            return
        except:
            pass