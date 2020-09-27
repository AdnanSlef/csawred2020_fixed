#!/usr/bin/env python3

from pwn import *

conn = remote('web.red.csaw.io',5016)

table = { '{':'}',
          '}':'{',
          '/':'\\',
          '\\':'/',
          '[':']',
          ']':'[',
}

def whack(board):
    boxheight = 0
    while len(board[boxheight].strip()):
        boxheight+=1
    while not(len(board[boxheight].strip())):
        boxheight+=1

    i = 0
    while board[i][0]==' ':
        i+=1
    c = board[i][0]
    width = ( board[i].count(c) + (board[i].count(table[c]) if c in table else 0) )//2 #wrong if this char is used inside the box

    print('Box hight:',boxheight)
    print('Total width:',width)

    height = len(board) // boxheight
    boxwidth = len(board[0]) // width
    
    print('Total height:',height)
    print('Box width:',boxwidth)
    
    for row in range(height):
        for col in range(width):
            if board[row * boxheight + 1][col * boxwidth + (boxwidth//2-1)] == '_':
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
    if score >= 9950:
        print(conn.recv().decode())

for lvl in range(1000):
    try:
        playlevel()
    except EOFError:
        print('Died at',lvl)
        print('If no flag, just run again. May take 5-10 attempts if unlucky.')
        break

conn.close()
