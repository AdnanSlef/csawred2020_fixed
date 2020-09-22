#!/usr/bin/env python3

from pwn import *

conn = remote('pwn.red.csaw.io', 5010)

def menuChoice(n):
    print(conn.recvuntil('(4) Begin Hacking\n> ').decode())
    conn.sendline(str(n).encode())

def createCharacter(name):
    assert len(name) <= 15
    menuChoice(1)
    print(conn.recvuntil(b'Enter your character\'s name:\n>').decode())
    conn.sendline(name)
    print(conn.recvuntil(b'joined your party!\n').decode())

def viewCharacter(index):
    menuChoice(2)
    print(conn.recvuntil(b'Which character do you wish to view (0-5)? \n>').decode())
    conn.sendline(str(index).encode())
    sep = b'-----------------------------\n'
    print((conn.recvuntil(sep)+conn.recvuntil(sep)+conn.recvuntil(sep)).decode())

def renameCharacter(index, name):
    assert len(name) <= 15
    menuChoice(3)
    print(conn.recvuntil(b'wish to rename (0-5)? \n>').decode())
    conn.sendline(str(index).encode())
    print(conn.recvuntil(b'name:\n>').decode())
    conn.sendline(name)
    print(conn.recvuntil(b'Rename complete.\n').decode())

createCharacter(b'freddy')
viewCharacter(0)
renameCharacter(0,b'mercury')
viewCharacter(0)

conn.interactive()

conn.close()
