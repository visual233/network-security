# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 13:54:24 2019

@author: WXS
"""

import socket
import select
import sys

# creat socket and set the port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',9999))

#wait and accept the info of other host
s.listen(1)
conn, addr = s.accept()

read_handler = [sys.stdin, conn]

while True:
    ready_to_read, _, _ = select.select(read_handler, [], [])
    
    if sys.stdin in ready_to_read:
        user_input = input()
        conn.send((user_input+'\n').encode('utf-8'))
        
    if conn in ready_to_read:
        data = conn.recv()
    
