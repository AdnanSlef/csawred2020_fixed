#!/usr/bin/env python3

from pwn import *

with open('spaghetti.c','r') as f:
    original = f.read()

def gather_definitions(code):
    definitions = {}
    for line in code.split('\n'):
        if 'define' in line:
            l = len(line.split()[1])
            definition = line.split()[-1]
            definitions[l] = definition
    return definitions

def interpret(code, definitions):
    output = ''
    header = True
    for line in code.split('\n'):
        if 'define' in line:
            header = False
        elif header:
            #output += line + '\n'
            continue
        else:
            words = line.split()
            output += ''.join(definitions[len(w)]for w in words)
    return output
                
print(interpret(original,gather_definitions(original)))

conn = remote('rev.red.csaw.io',5001)
conn.sendline(b'CPU:GenuineIntel')
print(conn.recv().decode())
conn.close()

