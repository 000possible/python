#!/usr/bin/python 3
# -*- coding:utf-8 -*-

import socket
from .packet import *

def scansyn(src, sport, dst, dport):
    try:
        sock_send = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        sock_recv = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    except socket.error as msg:
        print("socket could not be create %s " % msg.strerror)
        sys.exit()

    try:
        sock_recv.bind((src, sport))
    except socket.error as msg:
        print("socket bind interface error %s " % msg.strerror)
        sys.exit()
    #make tcp packet
    pack = make_pack(src, sport, dst, dport)
    #send tcp packet
    sock_send.sendto(pack, (dst, 0))
    #sniffer recv syn ack packet
    result,addr = sock_recv.recvfrom(65535)
    #clear socket
    sock_send.close()
    sock_recv.close()

    return (result, addr)


