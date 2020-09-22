#!/usr/bin/env python3

from pwn import *
from z3 import *

def solve1():
    passcode = [
0x6e5f6c6c69775f75,
0x6575675f72657665,
0x5f736968745f7373,
0x5f65737561636562,
0x6c5f6f735f737469,
0x676e6f
    ]
    return b''.join(i.to_bytes(8,'little')for i in passcode).replace(b'\0',b'')

def solve2():
    A = BitVec('a',32)
    b = 50
    assert b >= 0x32
    B = BitVecVal(b,32)
    C = BitVec('c',32)
    cond_initial_C = A==C
    working_C = BitVec('cw',32)
    for i in range(b,0,-1):
        I = BitVecVal(i,32)
        working_C = working_C ^ B + A * I
    cond_final_C = working_C == 0x7a69#BitVecVal(0x7a69,32)
    cond_min_A = UGT(A,BitVec(0x32,32))
    cond_int_A = ULE(A,BitVec(214748364,32))

    slvr = Solver()
    slvr.add(cond_initial_C)
    slvr.add(cond_final_C)
    slvr.add(cond_min_A)
    slvr.add(cond_int_A)
    
    print(slvr.check())
    print(slvr.model())
    print(slvr.model()[A])

    a = slvr.model()[A] #replace with computed a
    return str(a)+' '+str(b)

def brute2(d):
    def check(a,b):
        u32 = 0xffffffff
        c = a
        i = b
        while 0<i:
            c = (c ^ b) & u32
            c = (c + ((a*i) & u32) ) & u32
            i = i - 1
        return c == 0x7a69 #31337
    for a in range(0x32, 0x32+d):
        for b in range(0x32,0x32+d):
            if check(a, b):
                print(f'a{a} b{b}')
    print('returned')

#brute2(500)

sol1 = solve1()
sol2 = solve2()

conn = remote('rev.red.csaw.io',5002)

print(conn.recv().decode())

print(sol1)
conn.sendline(sol1)

print(conn.recv().decode())

print(sol2)
conn.sendline(sol2)

print(conn.recv().decode())

conn.interactive()
conn.close()
