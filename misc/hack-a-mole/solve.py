#!/usr/bin/env python3

from pwn import *

conn = remote('web.red.csaw.io',5016)

def whack(board):
    height = len(board) // 9
    width = len(board[0]) // 18
    print('height:',height,'; width:',width)
    for row in range(height):
        for col in range(width):
            if board[row * 9 + 1][col * 18 + 8] == '_':
                return row,col
    print("Where's the mole??")
    return 0, 0

def playlevel():
    print(conn.recvuntil('Level: ').decode())
    lvl = int(conn.recvuntil(' ').strip())
    print(lvl)
    print(conn.recvuntil('Score: ').decode().strip())
    score = int(conn.recvuntil('\n\n').strip())
    print(score)
    board_andmore = conn.recvuntil('Whack (row col): ')
    print(board_andmore.decode())
    board = board_andmore[:-len('\n\nWhack (row col): ')].decode().split('\n')
    a, b = whack(board)
    print(a, b)
    conn.sendline(f'{a} {b}')

for i in range(1000):
    playlevel()

conn.interactive()

conn.close()
