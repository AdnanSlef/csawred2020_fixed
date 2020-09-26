#!/usr/bin/env python3

from pwn import *

conn = remote('crypto.red.csaw.io',5012)

print(conn.recv())

#Solve chall here

conn.interactive()

conn.close()
