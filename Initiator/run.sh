#!/bin/bash

n=8

for i in {0..7} 
do
  echo $i 
  let "port=2345+$i"
  python3.4 localproxy.py $port &
  sleep 0.1
done
