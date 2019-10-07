import argparse
import socket
import select
import basicim_nugget_pb2
import sys
import struct
from Crypto.Cipher import AES
import random, string
import hashlib
import hmac

parser = argparse.ArgumentParser()
parser.add_argument('-p', dest='port', help='port', required=True)
parser.add_argument('-n', dest='nickname', help='your nickname', required=True)
parser.add_argument('-s', dest='server', help='server', required=True)
parser.add_argument('-c', dest='confidentialitykey', required=True)
parser.add_argument('-a', dest='authenticitykey', required=True)

args = parser.parse_args()
iv = ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(16)).encode('utf-8')

def add_length(s):
    l = 32
    count = len(s)
    add = 0
    if count % l != 0:
        add = l - (count % l)
    s += '\0' * add
    return s

def encryption(s, key):
    # key = args.confidentialitykey
    s = add_length(s)
    key = add_length(key)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(s)
    return cipher_text

def decryption(c_s, key):
    # key = args.confidentialitykey
    key = add_length(key)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    plain_text = cipher.decrypt(c_s)
    return bytes.decode(plain_text).rstrip('\0')

def authentic_encode(s, key):
    # k = args.authenticitykey
    hm = hmac.new(key.encode('utf-8'), s, hashlib.sha256)
    return hm.hexdigest()


def main():

    # connect to server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect( (args.server,int(args.port)) )

    read_fds = [ sys.stdin, s ]
    key_e = args.confidentialitykey
    key_a = args.authenticitykey

    while True:
        (ready_list,_,_) = select.select(read_fds,[],[])
        if sys.stdin in ready_list:
            user_input = input()
            if user_input.rstrip().lower() == "exit":
                s.close()
                exit(0)
            nugget = basicim_nugget_pb2.BasicIMNugget()
            #encrypt message
            en_message = encryption(user_input, key_e)
            en_name = encryption(args.nickname, key_e)
            nugget.nickname = en_name
            nugget.au_message = authentic_encode(en_message+iv, key_a)
            nugget.en_message = en_message
            nugget.iv = iv

            serialized = nugget.SerializeToString()
            serialized_len = len(serialized)
            s.send( struct.pack("!H", serialized_len ) )
            s.send( serialized )
        if s in ready_list:
            packed_len = s.recv(2,socket.MSG_WAITALL)
            unpacked_len = struct.unpack("!H", packed_len )[0]
            serialized = s.recv(unpacked_len,socket.MSG_WAITALL)
            nugget = basicim_nugget_pb2.BasicIMNugget()
            nugget.ParseFromString(serialized)

            #verify and decrypt
            name = nugget.nickname
            enm = nugget.en_message
            aum = nugget.au_message
            r_iv = nugget.iv
            auth = authentic_encode(enm+r_iv, key_a)
            if auth == aum:
                m = decryption(enm, key_e)
                n = decryption(name, key_e)
                print("%s: %s" % (n, m), flush=True)
            else:
                s.close()
                exit(0)


if __name__ == '__main__':
    main()
