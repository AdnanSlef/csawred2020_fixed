#!/bin/bash
numlines=$(tshark -r otherplane.data -e data -Tfields -Y 'ip.dst == 10.15.200.47' | wc -l)
tshark -r otherplane.data -e data -Tfields -Y 'ip.dst == 10.15.200.47' | head -n $((numlines-1)) | tail -n $((numlines-3)) | xxd -ps -r > image.jpg
echo "Extracted image.jpg"
echo 'View image.jpg to find password "galactic octopus"'
echo
echo 'galactic octopus' | nc web.red.csaw.io 5019
echo
