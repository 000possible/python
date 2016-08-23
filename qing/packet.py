#!/usr/bin/env python3.4
# -*- coding:utf-8 -*-

import sys
import socket
import struct
import array
import random

def ip_header(src_ip,dst_ip):
    ip_ihl = 5
    ip_ver = 4
    ip_tos = 0
    ip_tot_len = 0
    ip_id = 54321
    ip_frag_off = 0
    ip_ttl = 255
    ip_proto = socket.IPPROTO_TCP
    ip_check = 0
    ip_saddr = socket.inet_aton(src_ip)
    ip_daddr = socket.inet_aton(dst_ip)
    ip_ihl_ver = (ip_ver << 4) + ip_ihl

    return struct.pack('!BBHHHBBH4s4s',
                       ip_ihl_ver,
                       ip_tos,
                       ip_tot_len,
                       ip_id,
                       ip_frag_off,
                       ip_ttl,
                       ip_proto,
                       ip_check,
                       ip_saddr,
                       ip_daddr)


def tcp_header(src_ip, sport, dst_ip, dport, data):
    tcp_source = sport
    tcp_dest   = dport
    tcp_seq = 454
    tcp_ack_seq = 0
    tcp_doff = 5
    tcp_fin = 0
    tcp_syn = 1
    tcp_rst = 0
    tcp_psh = 0
    tcp_ack = 0
    tcp_urg = 0
    tcp_window = socket.htons(3000)
    tcp_check = 0
    tcp_urg_ptr = 0
    tcp_offset_res = (tcp_doff << 4) +0
    tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5)

    tcp_head =  struct.pack('!HHLLBBHHH',
                       tcp_source,
                       tcp_dest,
                       tcp_seq,
                       tcp_ack_seq,
                       tcp_offset_res,
                       tcp_flags,
                       tcp_window,
                       tcp_check,
                       tcp_urg_ptr)
    sourct_address = socket.inet_aton(src_ip)
    dest_address   = socket.inet_aton(dst_ip)
    placeholder = 0
    protocol = socket.IPPROTO_TCP
    tcp_length = len(tcp_head)
    psh = struct.pack('!4s4sBBH',
                      sourct_address,
                      dest_address,
                      placeholder,
                      protocol,
                      tcp_length)
    psh = psh + tcp_head
    tcp_check = checksum(psh)

    return struct.pack('!HHLLBBHHH',
                       tcp_source,
                       tcp_dest,
                       tcp_seq,
                       tcp_ack_seq,
                       tcp_offset_res,
                       tcp_flags,
                       tcp_window,
                       tcp_check,
                       tcp_urg_ptr)


#
#  tcp checksum function copy from scapy project
#
def checksum(pkt):
    if struct.pack("H", 1) == b"\x00\x01":  # big endian
        if len(pkt) % 2 == 1:
            pkt += b"\0"
        s = sum(array.array("H", pkt))
        s = (s >> 16) + (s & 0xffff)
        s += s >> 16
        s = ~s
        return s & 0xffff
    else:
        if len(pkt) % 2 == 1:
            pkt += b"\0"
        s = sum(array.array("H", pkt))
        s = (s >> 16) + (s & 0xffff)
        s += s >> 16
        s = ~s
        return (((s >> 8) & 0xff) | s << 8) & 0xffff


def make_pack(src_ip, sport, dst_ip, dport, data=''):
    ip_head = ip_header(src_ip, dst_ip)
    tcp_head = tcp_header(src_ip, sport, dst_ip, dport, data)

    return ip_head + tcp_head