#!/usr/bin/env python3

from pwn import *

conn = remote('web.red.csaw.io',5016)

def playlevel():
    print(conn.recvuntil('Level: ').decode())
    lvl = int(conn.recvuntil(' ').strip())
    print(lvl)
    print(conn.recvuntil('Score: ').decode().strip())
    score = int(conn.recvuntil('\n\n').strip())
    print(score)
    board = conn.recv()
    print(board)
    print(board.decode())
    print(conn.recv())

playlevel()

conn.interactive()

conn.close()
