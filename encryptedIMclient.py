import argparse
import socket
import select
import prototest_pb2
import sys
import struct
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import hashlib
import hmac

parser = argparse.ArgumentParser()
parser.add_argument('-n', dest='nickname', help='your nickname', required=True)
parser.add_argument('-s', dest='server', help='server', required=True)
parser.add_argument('-c', dest='confidentialitykey', required=True)
parser.add_argument('-a', dest='authenticitykey', required=True)

args = parser.parse_args()

def encryption(s):
    key = args.confidentialitykey
    cipher = AES.new(key, AES.MODE_CBC, key)
    l = 32
    count = len(s)
    add = 0
    if count % l != 0:
        add = l - (count%l)
    s += '\0'*add
    cipher_text = cipher.encrypt(s)
    return b2a_hex(cipher_text)

def decryption(c_s):
    key = args.confidentialitykey
    cipher = AES.new(key, AES.MODE_CBC, key)
    plain_text = cipher.decrypt(a2b_hex(c_s))
    return plain_text

def authentic_encode(s):
    k = args.authenticitykey
    hm = hmac.new(k, s, hashlib.sha256)
    return hm.hexdigest()


def main():

    # connect to server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect( (args.server,9999) )

    read_fds = [ sys.stdin, s ]

    while True:
        (ready_list,_,_) = select.select(read_fds,[],[])
        if sys.stdin in ready_list:
            user_input = input()
            if user_input.rstrip().lower() == "exit":
                s.close()
                exit(0)
            nugget = prototest_pb2.BasicIMNugget()
            nugget.nickname = args.nickname
            #encrypt message
            en_message = encryption(user_input)
            au_message = authentic_encode(en_message)
            nugget.message = au_message + ',' + en_message

            serialized = nugget.SerializeToString()
            serialized_len = len(serialized)
            s.send( struct.pack("!H", serialized_len ) )
            s.send( serialized )
        if s in ready_list:
            packed_len = s.recv(2,socket.MSG_WAITALL)
            unpacked_len = struct.unpack("!H", packed_len )[0]
            serialized = s.recv(unpacked_len,socket.MSG_WAITALL)
            nugget = prototest_pb2.BasicIMNugget()
            nugget.ParseFromString(serialized)

            #verify and decrypt
            receive = nugget.message.split(',')
            auth = authentic_encode(receive[1])
            if auth == receive[0]:
                m = decryption(receive[1])
                print("%s: %s" % (nugget.nickname, m), flush=True)
            else:
                s.close()
                exit(0)


if __name__ == '__main__':
    main()
    
