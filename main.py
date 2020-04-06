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
output = bytearray(16)  #the output program
outputIndex = 0
index = 0

def CheckIfRegister(checkVar):
	
	if checkVar[0] == 't' or checkVar[0] == 'T':
		return 0

	if checkVar[0] == 'p' or checkVar[0] == 'P':
		return 1
	
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
	filein = input("file name: ")


with open(filein, "r") as f:
	lines = f.readlines()

for line in lines:#just testing file reading
	if line == '\n':
		print("empty line")
	else:
		print(str(line), end='')
print('\n')

#commented out, not yet needed
'''for lineIndex, line in enumerate(lines):
	index = 0
	if (line[0] != ' ') and (line[0] != '	') and (line[0] != '\n') and (line[0] != ';'): #label
		print("found a label at line " + str(lineIndex + 1) + ' called: ', end='')
		splitTemp = line.split(':')
		print(splitTemp[0])
		labels[splitTemp[0]] = lineIndex
	else:
		if line[index] == ';':
			print("found a comment at line " + str(lineIndex + 1))

print(labels) '''

'''for lineIndex, line in enumerate(lines):
	inComment = False
	inFunction = False
	currCharacter = 0

	if line[0] == ' ' or line[0] == '	': #is the line not a label?
		while currCharacter < len(line):
			if line[currCharacter] == ';':
				inComment = True

			print(currCharacter, end='	')
			print(line[currCharacter], end=' ')
			print(inComment)

			#instruction finding
			if inComment == False and line[currCharacter] != ' ' and line[currCharacter] != '	':
				print("found a function thingy")
				tempSplit = line[currCharacter:].split(' ')
				print("tempSplit: " + str(tempSplit[0]))
				currCharacter += len(tempSplit[0])
				
				checkPart(tempSplit[0])
			currCharacter += 1
	else:
		pass '''
		
#how it should be done:
#1: split line up into parts, split by a space.
#2: work through if-else tree for selecting correct opcode

for lineIndex, line in enumerate(lines):
	tempSplit = line.split(' ')
	print(str(tempSplit))

	#is line indented?
	tempFind = tempSplit[0].find("\t")
	if tempFind == 0:  #we found an indented part

		#LD operand
		if tempSplit[0].find("ld") == 1 or tempSplit[0].find("LD") == 1: #if command is ld or LD, expects 2 operands
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










#input("hit enter to end program")



