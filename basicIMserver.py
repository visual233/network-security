# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 13:54:24 2019
@author: WXS
"""

import socket
import select
import sys
import signal
import prototest_pb2 as pb

# creat socket and set the port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 9999))
conn_list = []
# wait and accept the info of other host
s.listen(1)

read_handler = [sys.stdin, s]


def handler(signum, frame):
    print("Bye!")
    s.close()  # I'm assuming s is your bind/listen socket; replace with correct varname if necessary
    sys.exit(0)


signal.signal(signal.SIGINT, handler)

while True:
    ready_to_read, _, _ = select.select(read_handler, [], [])
    proto = pb.Chat()

    for c in ready_to_read:
        if c is s:
            conn, addr = s.accept()
            conn_list.append(conn)
            read_handler.append(conn)

        elif c is sys.stdin:
            user_input = input()
            proto.name = 'server'
            proto.msg = user_input
            msg_ser = proto.SerializeToString()
            s.send(msg_ser)

        else:
            data = c.recv(1024)
            if len(data) == 0 and c in conn_list:
                conn_list.remove(c)
                continue
            proto.SerializeToString(data)
            print(proto.name+':'+proto.msg, flush=True)
            proto_ser = proto.SerializeToString()
            for con in conn_list:
                con.send(proto_ser)