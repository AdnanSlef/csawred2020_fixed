#!/usr/bin/env python3

from pwn import *
from base64 import b64decode, b64encode

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

# encrypts b'Your application has been REJECTED'
# using a random IV in CTR mode
def get_ct():
    conn.sendlineafter('> ','1')
    conn.sendlineafter('> ','')
    conn.recvuntil('Token: ')
    token = b64decode(conn.recvuntil('\r\n').strip())
    iv = token[:16]
    ct = token[16:]
    return iv, ct

def process(msg):
    msg = b64encode(msg)
    conn.sendlineafter('> ','2')
    conn.sendlineafter('> ',msg)

given  = b'Your application has been REJECTED'
target = b'Your application has been ACCEPTED'
difference = byte_xor(given, target)

conn = remote('crypto.red.csaw.io',5012)

iv, ct = get_ct()

msg = iv + byte_xor(ct,difference)

process(msg)

print(conn.recvall().decode())

conn.close()
