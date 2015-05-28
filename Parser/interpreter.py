
def interpreter(list):
	file = open("SampleCode.chng","r")
	for num, line in enumerate(file, 1):					#line is literally just what the string in the line is, num is what line number
		if num == list[1]:									#given our list from parser, we check if our current line number is what we want to parse
			if list[0] == "Print"							#conditions to what to translate chingchong into
				printList = line.split("I show Father")		#take away what we dont want
				printList = printList[1].split(" lah")		#take away the other side
				writeString = "print " + printList[0]		#writeString is what we want to write to the python file
				print writeString
		
		
list = ["Print",54]
interpreter(list)
