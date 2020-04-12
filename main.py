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
labels = {}
output = bytearray(32)  #the output program
outputIndex = 0
index = 0

def CheckIfRegister(checkVar):
	
	if checkVar[0] == 't' or checkVar[0] == 'T': #temp / swap
		return 0

	if checkVar[0] == 'p' or checkVar[0] == 'P': #pointer (for memory read/writes)
		return 1

	if checkVar[0] == 'a' or checkVar[0] == 'A': #Accumulator, read-only, only updated after ALU instruction
		return 2
	
	if checkVar[0:2] == 'i1' or checkVar[0:2] == 'I1': #ALU in 1
		return 3

	if checkVar[0:2] == 'i2' or checkVar[0:2] == 'I2': #ALU in 2
		return 4

	
	if checkVar[0] == 'b' or checkVar[0] == 'B': #memory bank
		return 0xD
	
	if checkVar[0:3] == 'in1' or checkVar[0:3] == 'IN1': #hex keypad input 0-7, read-only
		return 0xE
	
	if checkVar[0:3] == 'in2' or checkVar[0:3] == 'IN2': #hex keypad input 8-F, read-only
		return 0xF
	
	return - 1
	
def CheckData(checkVar):

	if str(checkVar).find('0x') == 0:
		return int(checkVar[2:], 16)
	
	if str(checkVar).find('%') == 0:
		return int(checkVar[1:], base=2)

	if checkVar[0:].isdigit() == True:
		return int(checkVar[0:], base=10) #decimal has no identifier, so we check if it's a number

	return -1

#getting the input filename
if len(sys.argv) != 1: #if a filename is supplied through launch args
	filein = sys.argv[1]
else: #if no filename is supplied through launch args, promt user
	filein = input("input file name: ")

if len(sys.argv) > 2:  #if both a input-filename and output-filename are supplied
	fileout = sys.argv[2]
else:
	fileout = input("output file name: ")

with open(filein, "r") as f:
	lines = f.readlines()

for line in lines:#just testing file reading
	if line == '\n':
		print("empty line")
	else:
		print(str(line), end='')
print('\n')



for lineIndex, line in enumerate(lines):
	tempSplit = line.split(' ')
	print(str(tempSplit))

	#is line indented?
	tempFind = tempSplit[0].find("\t")
	if tempFind == 0 and tempSplit[0].find(';') != 1:  #we found an indented part (and it's not a comment)
		
		if tempSplit[0].find('and') == 1 or tempSplit[0].find('AND') == 1:
			#i1 AND i2 -> acc
			output[outputIndex] = 0x00
			outputIndex += 1
			output[outputIndex] = 0x01
			outputIndex += 1
			print(str(list(output)))

		elif tempSplit[0].find('or') == 1 or tempSplit[0].find('OR') == 1:
			#i1 OR i2 -> acc
			output[outputIndex] = 0x00
			outputIndex += 1
			output[outputIndex] = 0x02
			outputIndex += 1
			print(str(list(output)))

		elif tempSplit[0].find('nand') == 1 or tempSplit[0].find('NAND') == 1:
			#i1 OR i2 -> acc
			output[outputIndex] = 0x00
			outputIndex += 1
			output[outputIndex] = 0x03
			outputIndex += 1
			print(str(list(output)))

		elif tempSplit[0].find('xor') == 1 or tempSplit[0].find('XOR') == 1:
			#i1 OR i2 -> acc
			output[outputIndex] = 0x00
			outputIndex += 1
			output[outputIndex] = 0x04
			outputIndex += 1
			print(str(list(output)))

		elif tempSplit[0].find('rl') == 1 or tempSplit[0].find('RL') == 1:
			#i1 OR i2 -> acc
			output[outputIndex] = 0x00
			outputIndex += 1
			output[outputIndex] = 0x05
			outputIndex += 1
			print(str(list(output)))

		elif tempSplit[0].find('rr') == 1 or tempSplit[0].find('RR') == 1:
			#i1 OR i2 -> acc
			output[outputIndex] = 0x00
			outputIndex += 1
			output[outputIndex] = 0x06
			outputIndex += 1
			print(str(list(output)))

		elif tempSplit[0].find('jpz') == 1 or tempSplit[0].find('JPZ') == 1:
			#jump if zero
			output[outputIndex] = (CheckData(tempSplit[1]) >> 8) | 0x20
			outputIndex += 1
			output[outputIndex] = (CheckData(tempSplit[1]) & 0xFF)
			outputIndex += 1
			print(str(list(output)))

		elif tempSplit[0].find('jpn') == 1 or tempSplit[0].find('JPN') == 1:
			#jump if NOT zero
			output[outputIndex] = (CheckData(tempSplit[1]) >> 8) | 0x30
			outputIndex += 1
			output[outputIndex] = (CheckData(tempSplit[1]) & 0xFF)
			outputIndex += 1
			print(str(list(output)))

		elif tempSplit[0].find('jp') == 1 or tempSplit[0].find('JP') == 1:
			#jump absolute
			output[outputIndex] = (CheckData(tempSplit[1]) >> 8) | 0x10
			outputIndex += 1
			output[outputIndex] = (CheckData(tempSplit[1]) & 0xFF)
			outputIndex += 1
			print(str(list(output)))

		

		#LD operand
		elif tempSplit[0].find("ld") == 1 or tempSplit[0].find("LD") == 1: #if command is ld or LD, expects 2 operands
			print(tempSplit[1])
			print(tempSplit[2])

			#LD REG VALUE
			if CheckIfRegister(tempSplit[1]) != -1 and CheckData(tempSplit[2]) != -1:
				print("first operand is register " + str(CheckIfRegister(tempSplit[1])))
				print("second operand is value " + str(CheckData(tempSplit[2])))

				#ld VALUE into temp
				output[outputIndex] = 0x40
				outputIndex += 1
				output[outputIndex] = CheckData(tempSplit[2])
				outputIndex += 1
				
				#ld temp into REG
				output[outputIndex] = 0x43
				outputIndex += 1
				output[outputIndex] = ((0x0 << 4) | CheckIfRegister(tempSplit[1]))
				outputIndex += 1

			#LD VALUE REG
			elif CheckData(tempSplit[1]) != -1 and CheckIfRegister(tempSplit[2]) != -1:
				print("UNIMPLEMENTED LD VERSION AT LINE " + str(lineIndex))
				print("first operand is value " + str(CheckData(tempSplit[1])))
				print("second operand is register " + str(CheckIfRegister(tempSplit[2])))

				#ld 

			#LD VALUE VALUE
			elif CheckData(tempSplit[1]) != -1 and CheckData(tempSplit[2]) != -1:
				print("UNIMPLEMENTED LD VERSION AT LINE " + str(lineIndex))

			#LD REG REG
			elif CheckIfRegister(tempSplit[1]) != -1 and CheckIfRegister(tempSplit[2]) != -1:
				print("first operand is register " + str(CheckIfRegister(tempSplit[1])))
				print("second operand is register " + str(CheckIfRegister(tempSplit[2])))

				#ld REG2 into REG1
				output[outputIndex] = 0x43
				outputIndex += 1
				output[outputIndex] = ((CheckIfRegister(tempSplit[2]) << 4) | CheckIfRegister(tempSplit[1]))
				outputIndex += 1
			print(str(list(output)))

		

		


writefile = open(fileout, "wb")
fileIndex = 0
while fileIndex < outputIndex:
	writefile.write((output[fileIndex]).to_bytes(1,byteorder="little"))
	fileIndex += 1
writefile.close()







#input("hit enter to end program")



