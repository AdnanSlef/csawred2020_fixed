#!/usr/bin/env python3

from itertools import permutations

code = (
 '5025015500'
+'0150525150'
+'2551555201'
+'5500215255'
+'1502001522'
+'0150552150'
+'0051222215'
+'0002150552'
+'1550251502'
+'2215255155'
+'0001550001'
+'5555215552'
+'21'
)

code = code.replace('0','R').replace('1','\n').replace('2','S').replace('5','P')

print('code:',code)
print('len:',len(code))

candidates = []
for R,P,S in ['012','021','102','120','201','210']:
    m = code.replace('R',R).replace('P',P).replace('S',S)
    print(m)
    m = ' '.join(str(int(i,3))for i in m.split())
    print(m)
    m = ''.join(chr(int(c))for c in m.split())
    print(m)
    if 'flag' in m:
        candidates.append(m)

print('\n\n')
for c in candidates:
    print(c)
