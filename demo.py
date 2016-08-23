#!/usr/bin/python 3
# -*- coding:utf-8 -*-

import sys
import socket
import struct
import array
import random
import argparse
from qing import socksr


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='network demo')
    parser.add_argument('--src', type=str)
    parser.add_argument('--sport', type=int)
    parser.add_argument('--dst', type=str)
    parser.add_argument('--dport', type=int)
    args = parser.parse_args();
    print(args)
    result = socksr.scansyn(args.src, args.sport, args.dst, args.dport)
    print(result)