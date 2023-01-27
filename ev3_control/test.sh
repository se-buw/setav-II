#!/bin/bash
# echo hello 
# a="$(ifconfig | grep 192.168)"
# echo $a
# python3 /home/robot/.local/bin/rpyc_classic.py --host=0.0.0.0

#! /bin/bash

# Given string 
string=$(ifconfig)

# Setting IFS (input field separator) value as ","
IFS=' '

# Reading the split string into array
read -ra arr <<< "$string"

# Print each value of the array by using the loop
for val in "${arr[@]}";
do
  printf "name = $val\n"
done