#!/usr/bin/env python3

from pwn import *
from Crypto.Hash import MD5

prefix = b"Hi, my name is Jangui. My card is my passport. Please verify me."

def collide(payload):
    assert len(payload) == 400 - 256
    collisions = []
    i = 0
    while len(collisions)<2:
        msg = (prefix
              +str(i).encode()
              +b'A'*(256-len(prefix)-len(str(i)))
              +payload
              )
        h = MD5.new()
        h.update(msg)
        if h.hexdigest()[:2] == '00':
            collisions.append(msg)
        i+=1
    return collisions

payload = b'B'*144

ids = collide(payload)

conn = remote('web.red.csaw.io',5012)

print(conn.recvuntil('>'))
print(ids[0])
conn.send(ids[0])

print(conn.recvuntil('>'))
print(ids[1])
conn.send(ids[1])

print(conn.recv())

###WIN###

conn.interactive()

conn.close()
