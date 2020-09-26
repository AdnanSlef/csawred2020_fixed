#!/usr/bin/env python3

from pwn import *

conn = remote('nc web.red.csaw.io',5016)

print(conn.recv())


###WIN###

conn.interactive()

conn.close()
