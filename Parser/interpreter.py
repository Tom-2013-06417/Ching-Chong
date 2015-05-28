
def nextline(file, num):
	num = num + 1
	string = ""
	for num, line in enumerate(file, num):
		line = line.strip()
		if line == "I did not know lah.":
			return string
		if line =="to become doctor lah.":
			return string
		if "Sincerely, " in line:
			return string
		line = line.split(" lah")[0]
		
		string = string + line + "\n"
		
	


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
			if list[0] == "VarDecSegment":
				variablesDeclared = nextline(file, num)
				listedVars = variablesDeclared.split("\n")
				variableDict = {"Int":[],"Float":[],"Bool":[],"Char":[],"String":[],"List":[]}
				for i in listedVars:
				
					splitLine = i.split("\n")
					
					nameAndValue = splitLine[0].split(", ")
					splitDistinguish = nameAndValue[0].split(" ")
					print splitDistinguish [0]
					if splitDistinguish[0] == "GWA":
						
						variableDict["Float"].append(splitDistinguish[1])
						for i in range(1,len(nameAndValue)):
							variableDict["Float"].append(nameAndValue[i].split(" of ")[0])
					
					if splitDistinguish[0] == "Score":
						variableDict["Int"].append(splitDistinguish[1])
						for i in range(1,len(nameAndValue)):
							variableDict["Int"].append(nameAndValue[i].split(" of ")[0])
						
					
					if splitDistinguish[0] == "Honor":
						variableDict["Bool"].append(splitDistinguish[1])
						for i in range(1,len(nameAndValue)):
							variableDict["Bool"].append(nameAndValue[i].split(" of ")[0])
					if splitDistinguish[0] == "LetterGrade":
						variableDict["Char"].append(splitDistinguish[1])
						for i in range(1,len(nameAndValue)):
							variableDict["Char"].append(nameAndValue[i].split(" of ")[0])
						
					if splitDistinguish[0] == "Essay":
						variableDict["String"].append(splitDistinguish[1])
						for i in range(1,len(nameAndValue)):
							variableDict["String"].append(nameAndValue[i].split(" of ")[0])
						
					if splitDistinguish[0] == "ReportCard":
						variableDict["List"].append(splitDistinguish[1])
						for i in range(1,len(nameAndValue)):
							
							variableDict["List"].append(nameAndValue[i].split(" of ")[0])
					

				print variableDict
			if list[0] == "Arithmetic":
				inputList = line.split("Father surprise quiz: ")
				inputList2 = inputList[1].split(" lah")
				arith = inputList2[0]
				writeString = arith
				print writeString
			if list[0] == "ArithmeticBlock":
				writeString = nextline(file, num)
				print writeString
			if list[0] == "Break":
				breaker = "break"
				writeString = breaker
				print writeString
			if list[0] == "Continue":
				continuer = "continue"
				writeString = continuer
				print writeString
			if list[0] == "For":
				pass

			break

list = ["VarDecSegment", 5]
interpreter(list)
