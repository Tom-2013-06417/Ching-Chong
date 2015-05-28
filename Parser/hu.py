f=open("txt.txt")
lis=f.readlines()

tokens=[".", "Hi, I am", "I send shrimp friend rice to all:", "I want dumplings and:", "okay lah.", "Father says that I need:", "to become doctor lah.", "I give you sum", "I write to", "I get", "Teacher adds", "Teacher gets", "Father gets", "Father counts", "Teacher adds", "Father say make repeat", "Must do", "I show", "again lah.", "oclock lah.", "I'm done with", "Must repeat", "Father ask", "Father ask again", "I double confirm", "Father stop asking", "greaterer to", "more greaterer to", "lesser to", "more lesser to", "same to", "not same to", "I'm tired lah.", "Father brought out belt lah.", "I show father","Father wants", "I give father", "Father surprise quiz:", "Father surprise long quiz:", "I did not know lah."]

for i in range(0,len(lis)):
	#para sa mga newline
	if lis[i]=='\n':
		lis[i]=repr('\n')
	#para string ung newline at the end of the string
	lis[i]=lis[i].rstrip()+" "+repr('\n')
	#para matanggal ung mga spaces para sa comments
	lis[i]=' '.join(lis[i].split())
	#para matanggal ung comments
	ind=lis[i].find("-_-")
	if ind != -1:
		lis[i]=lis[i][0:ind-1]
	#######################################
	for j in tokens:
		str(j)
		index=lis[i].find(j)
		if index!=-1:
			first=lis[i][0:index-1]
			second=lis[i][index+len(j):len(lis[i])]
			#print first, "\n", second

#print lis
st=' '.join(lis)
print st