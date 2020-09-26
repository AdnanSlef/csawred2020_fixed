#!/bin/bash
strings recovery.data | grep -oPi '\w*alice\w*@\w*\.\w*' | nc web.red.csaw.io 5018
echo
