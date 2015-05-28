
def nextline(file, num):
	num = num + 1
	for num, line in enumerate(file, num):
		line = line.strip()
		if line == "I did not know lah.":
			return
		line = line.split(" lah")[0]
		print line
		


def interpreter(list):
	ArithFlag = False
	file = open("mySecondishProgram.chng","r")
	for num, line in enumerate(file, 1):					#line is literally just what the string in the line is, num is what line number
		line = line.strip()
		if num == list[1]:									#given our list from parser, we check if our current line number is what we want to parse
			if list[0] == "Print":							#conditions to what to translate chingchong into
				printList = line.split("I show Father")		#take away what we dont want
				printList = printList[1].split(" lah")		#take away the other side
				writeString = "print " + printList[0]		#writeString is what we want to write to the python file
				print writeString
			if list[0] == "Input":
				inputList = line.split("I give Father ")
				variable = inputList[1].split(" lah")[0]
				writeString = str(variable) + "= input()"
				print writeString
			if list[0] == "InputPrompt":
				inputList = line.split("Father wants ")
				inputList2 = inputList[1].split(", I give Father ")
				prompt = inputList2[0]
				variable = inputList2[1].split(" lah")[0]
				writeString = str(variable) + "= input(" + prompt + ")"
				print writeString
			if list[0] == "Arithmetic":
				inputList = line.split("Father surprise quiz: ")
				inputList2 = inputList[1].split(" lah")
				arith = inputList2[0]
				print arith
			if list[0] == "ArithmeticBlock":
				nextline(file, num)
			if list[0] == "Break":
				breaker = "break"
				print breaker
			if list[0] == "Continue":
				continuer = "continue"
				print continuer
			if list[0] == "For":
				pass

			break

list = ["ArithmeticBlock", 141]
interpreter(list)
