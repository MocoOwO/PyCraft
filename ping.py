import socket
import time
import Class
import json

from varint import *


def recv_one(sk):
    r = sk.recv(1)
    length = b''

    while r[0] > 128:
        length += r
        r = sk.recv(1)
    length += r
    length = de_varint(length)
    d = sk.recv(length)

    while len(d) != length:
        r = s.recv(length - len(d))
        d += r
    return d


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 25565
host = '127.0.0.1'
s.connect((host, port))

# s.send(b'\x10\x00\xFB\x05\x09localhost\x63\xDD\x01')
Class.Handshake(763, host, port, 0x01).send(s)
# s.send(b'\x01\x00')
Class.StatusRequest().send(s)

r = Class.StatusResponse(recv_one(s))
print(r)
Class.Ping().send(s)
t1 = time.time()
Class.Pong(recv_one(s))
t2 = time.time()
print("Ping:", round((t2 - t1) * 1000, 2), "ms")
