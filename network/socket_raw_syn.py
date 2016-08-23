#!/usr/bin/python 3
# -*- coding:utf-8 -*-
#
##############################################################
#                                                            #
#                                                            #
#      create by hing                                        #
#                                                            #
##############################################################

import sys
import socket
import struct
import array
import random


if __name__ == '__main__':
    try:
        sock_send = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        sock_recv = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        sock_recv.bind(("", 20))
    except socket.error as msg:
        print("socket could not be create %s " % msg.strerror)
        sys.exit()

    ip = "104.223.3.183"
    port = 80
    data_pack = make_pack(ip, port, 'test')
    sock_send.sendto(data_pack, ('104.223.3.183', 0))
    result, addr = sock_recv.recvfrom(65535)
    res_id = struct.unpack('!H', result[4:6])
    print("result is: %s " % res_id)
    sock_send.close()
    sock_recv.close()
