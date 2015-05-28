
def interpreter(list):
	file = open("SampleCode.chng","r")
	for num, line in enumerate(file, 1):					#line is literally just what the string in the line is, num is what line number
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
list = ["Input",16]
interpreter(list)
