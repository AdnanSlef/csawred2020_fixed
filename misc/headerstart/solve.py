#!/usr/bin/env python3

with open('myImageFile','rb') as f:
    img = f.read()

with open('outfile','wb') as f:
    f.write(bytes([0x89,0x50,0x4e,0x47]))
    f.write(img)
