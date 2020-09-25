#!/usr/bin/env python3

from pwn import *

if args.REMOTE:
    conn = remote('pwn.red.csaw.io',5008)
else:
    conn = gdb.debug('./worstcodeever', gdbscript=(''
         +'break display\n'
         +'commands\n'
         +'heap bins\n'#unfortunately this shows up before gef context
         +'end\n'
         +'c\n'#start automatically
        )
    )

""" Notes
sizeof(struct Friend) == 16
sizeof(union identifier) == 8
tcache is used when friends are freed
"""

def addfriend():#TODO params
    pass#TODO
    #set option to 1
    #set int human_name
    #if human_name != 0:
        #set char[63] name via fgets; send all 63 or use \n which will be replaced with \0 to end
    #else:
        #set int64 id
    #set int age

def removefriend():#TODO params
    pass#TODO
    #set option to 2
    #set index

def editfriend():#TODO params
    pass#TODO
    #set option to 4
    #set index
    #if friend_type[index] != 0:
        #set char[63] name via fgets; send all 63 or use \n which will not be replaced but \0 will be tacked on
    #else:
        #set int64 id
    #set int age

def display():#TODO params
    pass#TODO
    #set option to 3
    #set index
    
conn.interactive()

conn.close()
