

lookup = 'Start -> Initialize'
file = open("pt.txt","r")

for num, line in enumerate(file, 1):
	if lookup in line:
		print 'found at line:', num

