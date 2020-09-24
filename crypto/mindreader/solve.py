#!/usr/bin/env python3

from pwn import *
from base64 import b64encode as b64e, b64decode as b64d

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def getencryptedflag():
    print(conn.recvuntil(b'> ').decode())
    print('1')
    conn.sendline(b'1')
    print(conn.recvuntil(b'thinking: ').decode())
    flag_ct = conn.recvuntil(b'\r\n').strip()
    print(flag_ct)
    flag_ct = b64d(flag_ct)
    return flag_ct

def encryptdata(data):
    data = b64e(data)
    print(conn.recvuntil(b'> ').decode())
    print('2')
    conn.sendline(b'2')
    print(conn.recvuntil(b'> ').decode())
    print(data)
    conn.sendline(data)
    print(conn.recvuntil(b'thinking: ').decode())
    data_ct = conn.recvuntil(b'\r\n').strip()
    print(data_ct)
    data_ct = b64d(data_ct)
    return data_ct

conn = remote('crypto.red.csaw.io',5011)

flag_ct = getencryptedflag()

key_xor_1 = encryptdata(b'\x01'*len(flag_ct))

key = bytes([b^1 for b in key_xor_1])

print(flag_ct)
print(len(flag_ct))

print(key_xor_1)
print(key)
print(byte_xor(flag_ct,key))

print('\n'+byte_xor(flag_ct,key).split(b'}')[0].decode()+'}')
