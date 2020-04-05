#
#   A compiler for the simple nyaaComputer
#
#   made by Frain_Breeze and Sqeesqad



import sys
import cmd
from pathlib import Path
from enum import Enum, auto

#variable declaration
programLength = 0
labels = [[],[]] #first set contains label name, second contains line number
output = [] #the output program

#getting the input filename
if len(sys.argv) != 1: #if a filename is supplied through launch args
    filein = sys.argv[1]
else: #if no filename is supplied through launch args, promt user
    filein = input("file name: ")


with open(filein, "r") as f:
    lines = f.readlines()

for line in lines:#just testing file reading
    if line == '\n':
        print("empty line")
    else:
        print(str(line), end='')
print('\n')

#for line in lines:




input("hit enter to end program")



