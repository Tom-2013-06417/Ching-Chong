''' Forgive the messy code'''
''' Proper pt.txt looks something like this
        State	ACTION	GOTO
	+	*	(	)	a	$	A	E	T	F	id
0	 	 	s4	 	s6	 	 	1	2	3	5
1	s7	 	 	 	 	z	 	 	 	 	 
2	r2	s8	 	r2	 	r2	 	 	 	 	 
3	r4	r4	 	r4	 	r4	 	 	 	 	 
4	 	 	s4	 	s6	 	 	9	2	3	5
5	r6	r6	 	r6	 	r6	 	 	 	 	 
6	r7	r7	 	r7	 	r7	 	 	 	 	 
7	 	 	s4	 	s6	 	 	 	10	3	5
8	 	 	s4	 	s6	 	 	 	 	11	5
9	s7	 	 	s12	 	 	 	 	 	 	 
10	r1	s8	 	r1	 	r1	 	 	 	 	 
11	r3	r3	 	r3	 	r3	 	 	 	 	 
12	r5	r5	 	r5	 	r5	 	 	 	 	 
(literally copy past the table, add a tab before the first token(<+> in this example))
and a grammar.txt
A -> E
E -> E + T
E -> T
T -> T * F
T -> F
F -> ( E )
F -> id
id -> a

Inputting this should work here.
'''
def parseTableMaker():
	file=open("pt.txt","r")
	file.readline()
	string = file.readline()
	inputs=string.split("\t")
	lr_table = []
	for string in file:

		states = string.split("\t")

		inputs2 = []
		states2 = []


		for i in inputs:
			noN = i.split("\n")
			inputs2.append(noN[0])
		for i in states:
			noN = i.split("\n")
			if noN[0] == ' ':
				noN.pop(0)
				noN.insert(0,"x")
			try:
				noN[0] =int(noN[0])
			except ValueError:
				noN[0] = noN[0]
			states2.append(noN[0])
		states2.pop(0)
		'''dict = {}
		for i in range(len(states2)):

			key = inputs2[i]
			
			dict[key]=states2[i]'''
			
		lr_table.append(states2)
	inputs2.pop(0)
	lr_table.append(inputs2)

	return lr_table
def rules():
	file=open("grammar.txt","r")

	grammarDict = {}
	iter = 0
	for string in file:
		grammarLines = []
		list = string.split(" ")
		for i in list:
			noN = i.split("\n")
			grammarLines.append(noN[0])
		grammarDict[iter] = grammarLines
		iter +=1
	return grammarDict
