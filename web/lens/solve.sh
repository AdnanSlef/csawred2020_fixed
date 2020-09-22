#!/bin/bash
curl web.red.csaw.io:5009 2>/dev/null | grep -o 'flag{.*}'
