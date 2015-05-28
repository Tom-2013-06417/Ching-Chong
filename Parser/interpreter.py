
def conditional(cond):
	if cond == "Own":
		return True
	elif cond == "Disown":
		return False
	else:
		if "more greaterer to" in cond:
			split = "more greaterer to"
			val = ">"


		elif "greaterer to" in cond:
			split = "greaterer to"
			val = ">="

		elif "more lesser to" in cond:
			split = "more lesser to"
			val = "<"
		
		elif "lesser to" in cond:
			split = "lesser to"
			val = "<="

		elif "not same to" in cond:
			split = "not same to"
			val = "!="

		elif "same to" in cond:
			split = "same to"
			val = "=="

		else: 
			print "SYNTAX ERROR"
			return

		cond = cond.split(split)
		return cond[0] + val + cond[1]



#print conditional("C more greaterer to X")


def nextline(file, num, indents=0):
	num = num + 1
	string = ""
	for num, line in enumerate(file, num):
		line = line.strip()
		if line == "I did not know lah.":
			string = string[:-1]
			return string
		elif line =="to become doctor lah.":
			string = string[:-1]
			return string
		elif "Sincerely, " in line:
			string = string[:-1]
			return string
		else:
			line = '\t'*indents + line.split(" lah")[0]
			string = string + line + "\n"



def getEnder(file, num, label=0):
	num = num + 1
	loopend = "I'm done with " + str(label) + " lah."
	for num, line in enumerate(file, num):
		line = line.strip()
		if line == loopend:
			return num
	print "SYNTAX ERROR"



def interpreter(mainlist, n, indents=0):
	list = mainlist[n]
	file = open("dummycode.chng","r")
	writervar = '\t'*indents

	for num, line in enumerate(file, 1):					#line is literally just what the string in the line is, num is what line number
		line = line.strip()
		if num == list[1]:									#given our list from parser, we check if our current line number is what we want to parse
			if list[0] == "Print":							#conditions to what to translate chingchong into
				printList = line.split("I show Father")		#take away what we dont want
				printList = printList[1].split(" lah")		#take away the other side
				writervar = writervar + "print" + printList[0]		#writervar is what we want to write to the python file
				print writervar
			if list[0] == "Input":
				inputList = line.split("I give Father ")
				variable = inputList[1].split(" lah")[0]
				writervar = writervar + str(variable) + "= input()"
				print writervar
			if list[0] == "InputPrompt":
				inputList = line.split("Father wants ")
				inputList2 = inputList[1].split(", I give Father ")
				prompt = inputList2[0]
				variable = inputList2[1].split(" lah")[0]
				writervar = writervar + str(variable) + "= input(" + prompt + ")"
				print writervar
			if list[0] == "Arithmetic":
				inputList = line.split("Father surprise quiz: ")
				inputList2 = inputList[1].split(" lah")
				writervar = writervar + inputList2[0]
				print writervar
			if list[0] == "ArithmeticBlock":
				writervar = nextline(file, num, indents)
				print writervar
			if list[0] == "Break":
				writervar = writervar + "break"
				print writervar
			if list[0] == "Continue":
				writervar = writervar + "continue"
				print writervar
			if list[0] == "VarDecSegment":
				variablesDeclared = nextline(file, num)
				listedVars = variablesDeclared.split("\n")
				variableDict = {"Int":[],"Float":[],"Bool":[],"Char":[],"String":[],"List":[]}
				for i in listedVars:
				
					splitLine = i.split("\n")
					
					nameAndValue = splitLine[0].split(", ")
					splitDistinguish = nameAndValue[0].split(" ")
					#print splitDistinguish [0]
					if splitDistinguish[0] == "GWA":
						
						variableDict["Float"].append(splitDistinguish[1])
						try:
							if splitDistinguish [2] == "of":
								
								writeString = splitDistinguish[1] + " = " + splitDistinguish[3]
								print writeString 
						except IndexError:
							
							writeString = splitDistinguish[1]
							print writeString 
						for i in range(1,len(nameAndValue)):
							variableDict["Float"].append(nameAndValue[i].split(" of ")[0])
							writeString = str(nameAndValue[i].split(" of ")[0]) + " = "+str(nameAndValue[i].split(" of ")[1])
							print writeString
					if splitDistinguish[0] == "Score":
						variableDict["Int"].append(splitDistinguish[1])
						try:
							if splitDistinguish [2] == "of":
								
								writeString = splitDistinguish[1] + " = " + splitDistinguish[3]
								print writeString 
						except IndexError:
							
							writeString = splitDistinguish[1]
							print writeString 
						
						for i in range(1,len(nameAndValue)):
							
							variableDict["Int"].append(nameAndValue[i].split(" of ")[0])
							
							writeString = str(nameAndValue[i].split(" of ")[0]) + " = "+str(nameAndValue[i].split(" of ")[1])
							print writeString
					if splitDistinguish[0] == "Honor":
						
						variableDict["Bool"].append(splitDistinguish[1])
						try:
							
							if "Own" == str(splitDistinguish[3]):
								bool = "True"
							if "Disown" == str(splitDistinguish[3]):
								bool = "False"
							writeString = splitDistinguish[1] + " = " + bool
							print writeString 
							
						except IndexError:
							
							writeString = splitDistinguish[1]
							print writeString 
						
						for i in range(1,len(nameAndValue)):
							variableDict["Bool"].append(nameAndValue[i].split(" of ")[0])
							if "Own" == str(nameAndValue[i].split(" of ")[1]):
								bool = "True"
							else:
								bool = "False"
							writeString = str(nameAndValue[i].split(" of ")[0]) + " = " + bool
							print writeString
					if splitDistinguish[0] == "LetterGrade":
						try:
							if splitDistinguish [2] == "of":
								
								writeString = splitDistinguish[1] + " = " + splitDistinguish[3]
								print writeString 
						except IndexError:
							
							writeString = splitDistinguish[1]
							print writeString 
						variableDict["Char"].append(splitDistinguish[1])
						
						for i in range(1,len(nameAndValue)):
							variableDict["Char"].append(nameAndValue[i].split(" of ")[0])
							writeString = str(nameAndValue[i].split(" of ")[0]) + " = "+str(nameAndValue[i].split(" of ")[1])
							print writeString
					if splitDistinguish[0] == "Essay":

						variableDict["String"].append(splitDistinguish[1])
						try:
							if splitDistinguish [2] == "of":
								
								writeString = splitDistinguish[1] + " = " + splitDistinguish[3]
								print writeString 
						except IndexError:
							
							writeString = splitDistinguish[1]
							print writeString 
						for i in range(1,len(nameAndValue)):
							variableDict["String"].append(nameAndValue[i].split(" of ")[0])
							
							writeString = str(nameAndValue[i].split(" of ")[0]) + " = "+str(nameAndValue[i].split(" of ")[1])
							print writeString
					if splitDistinguish[0] == "ReportCard":
						variableDict["List"].append(splitDistinguish[1])
						for i in range(1,len(nameAndValue)):
							
							variableDict["List"].append(nameAndValue[i].split(" of ")[0])
							#writeString = str(nameAndValue[i].split(" of ")[0]) + str(nameAndValue[i].split(" of ")[1])
							#print writeString

				print variableDict
			if list[0] == "For":
				forList = line.split("Father say make repeat ")
				forList2 = forList[1].split(" again lah.")
				label = forList2[0]
				num = num + 1
				for num, newline in enumerate(file, num):
					condline = newline
					break

				condvar = condline.split(" from ")[0].split("Must do ")[1]
				condrng1 = condline.split(" from ")[1].split(" to ")[0]
				condrng2 = condline.split(" from ")[1].split(" to ")[1].split(" oclock")[0]

				writervar = writervar + "for " + condvar + " in range(" + condrng1 + "," + condrng2 + "):"
				print writervar
				limit = getEnder(file, num, label)
				try:
					while mainlist[n][1] < limit:
						n = n + 1
						if mainlist[n][1] > limit:
							indents = indents - 1
						n = interpreter(mainlist, n, indents+1)
				except IndexError:
					pass
				return n
			if list[0] == "While":
				whileList = line.split("Father say make repeat ")
				whileList2 = whileList[1].split(" again lah.")
				label = whileList2[0]
				num = num + 1
				for num, newline in enumerate(file, num):
					condline = newline
					break

				label2 = condline.split(" while ")[0].split("Must repeat ")[1]
				if label != label2:
					print "SYNTAX ERROR"
				cond = condline.split(" while ")[1].split(" lah.")[0]
				conditional2 = conditional(cond)

				writervar = writervar + "while " + conditional2
				print writervar
				limit = getEnder(file, num, label)
				try:
					while mainlist[n][1] < limit:
						n = n + 1
						if mainlist[n][1] > limit:
							indents = indents - 1
						n = interpreter(mainlist, n, indents+1)
				except IndexError:
					pass
			return n



#list = [["For", 191], ["For", 194], ["For", 197], ["Print", 199], ["Print", 202], ["ArithmeticBlock", 206], ["For", 212], ["For", 215], ["Print", 217], ["Print", 222]]
#list = [["While", 97], ["Print", 99], ["Arithmetic", 100], ["While", 101], ["Print", 103], ["Arithmetic", 104], ["While", 105], ["Print", 107], ["Arithmetic", 108]]
list = [["VarDecSegment",62]]
interpreter(list, 0)

