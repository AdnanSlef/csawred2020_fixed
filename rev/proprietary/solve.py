#!/usr/bin/env python3

from pwn import *

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

p1 = b'supersupersupersecretdrm'
p2 = b'nofreelunches-orsoftware'
p3 = b'pleasegivemunneytousedis'

password = byte_xor(byte_xor(p1,p2),p3)

conn = remote('rev.red.csaw.io',5004)

conn.sendline(password)

print(conn.recv().decode())

conn.close()
