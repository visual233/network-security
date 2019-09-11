# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 16:09:38 2019
@author: WXS
"""

import argparse
import socket
import select
import sys
import prototest_pb2 as pb

parser = argparse.ArgumentParser()
parser.add_argument('-s', dest='server', help='servername', required=True)
parser.add_argument('-n', dest='nickname', help='nickname', required=True)
args = parser.parse_args()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((args.server, 9999))

read_handler = [sys.stdin, s]

while True:
    ready_to_read, _, _ = select.select(read_handler, [], [])
    proto = pb.Chat()
    if sys.stdin in ready_to_read:
        user_input = input()
        if user_input == 'exit':
            break
        proto.name = args.nickname
        proto.msg = user_input
        msg_ser = proto.SerializeToString()
        s.send(msg_ser)

    if s in ready_to_read:
        m = s.recv(1024)
        if len(m) == 0:
            break
        proto.ParseFromString(m)
        print(proto.name, ': ', proto.msg, flush=True)