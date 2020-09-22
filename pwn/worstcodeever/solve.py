#!/usr/bin/env python3

from pwn import *

conn = remote('pwn.red.csaw.io', 5008)

def createCharacter(name):
    assert len(name) <= 15
    print(conn.recv().decode())
    conn.sendline(b'1')
    print(conn.recv().decode())
    conn.sendline(name)

def viewCharacter(index):
    print(conn.recv().decode())
    conn.sendline(b'2')
    print(conn.recv().decode())
    conn.sendline(str(index).encode())

def renameCharacter(index, name):
    assert len(name) <= 15
    print(conn.recv().decode())
    conn.sendline(b'3')
    print(conn.recv().decode())
    conn.sendline(str(index).encode())
    print(conn.recv().decode())
    conn.sendline(name)

#createCharacter(b'freddy')
#viewCharacter(0)
#renameCharacter(0,b'mercury')
#viewCharacter(0)

conn.interactive()

conn.close()
