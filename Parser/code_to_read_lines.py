file = open("mySecondishProgram.chng", "r")
line_of_code = 1

dict_of_line = {}

theinput = file.readlines()

for i in theinput:
	dict_of_line[line_of_code] = i  #.strip("\n") ???
	
	#put each line of code in a dictionary yo
	#key => line number; value => line of code
	
	print [i]
	
	
file.close()