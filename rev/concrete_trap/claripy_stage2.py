#!/usr/bin/env python3

from claripy import *

"""
def solve2_take1():
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
"""
u32 = 2**32

def take1():
    for b in range(50,400):
        if b%100==0:
            print('benchmark',b)
        A = BVS('a',32)
        assert b >= 0x32
        B = BVV(b,32)
        
        s = Solver()
        
        working_C = ['unused']+[BVS('cw'+str(i),32)for i in range(1,b+1)] + [A]
        for i in range(b,0,-1):
            s.add(working_C[i] == working_C[i+1] ^ B + A * BVV(i,32))
        s.add( working_C[1]==BVV(0x7a69,32) )
        s.add( SGE(A,BVV(0x32,32)) )
        
        if s.satisfiable():
            print('sat',b)
            print(s.eval(working_C[1],3))
            print(s.eval(A,5))
            for a in s.eval(A,5):
                print(check_stage2(a,b))
    
    
def check_stage2(a,b):
    c = a
    i = b
    while(0<i):
        c = (((c ^ b)%u32)+((a * i)%u32))%u32
        i = i + -1
    return c
    
print(hex(2**32))
take1()
