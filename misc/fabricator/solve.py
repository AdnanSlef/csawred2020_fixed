#!/usr/bin/env python3

from pwn import *

conn = remote('web.red.csaw.io',5012)

print(conn.recv())


###WIN###

conn.interactive()

conn.close()
