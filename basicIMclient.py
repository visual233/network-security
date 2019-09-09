# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 16:09:38 2019

@author: WXS
"""

import argparse
import socket
import select
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-s', dest='server', help='servername', required=True)
parser.add_argument('-n', dest='nickname', help='nickname', required=True)
args = parser.parse_args()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((args.server, 9999))

read_handler = [sys.stdin, s]

while True:
    ready_to_read, _, _ = select.select(read_handler, [], [])
    if sys.stdin in ready_to_read:
        user_input = input()
        if user_input == 'exit':
            sys.exit()
        msg = nickname + ': ' + user_input
        s.send(s)
        
    if s in ready_to_read:
        
        

