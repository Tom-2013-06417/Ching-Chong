from parseTableConverter import parseTableMaker
from parseTableConverter import rules
from hu import tokenizer

def find_index(ch): #this returns the index of the lexeme in the table
    i = 0
    lrMinOne = len(lr_table) - 1
    
    for i in range(len(lr_table[0])):
        if (lr_table[lrMinOne][i] == ch):
            return i
    

lr_table=parseTableMaker()

#ok check this so basta ganito lang yun format ng paglagay ng rule
#since dictionary siya, yung key is yung rule number
#yung value is yung dissected right part ng rule; dissected to tokens to ah, mahalaga yung '->' 


grammar_rules = rules()

the_input = tokenizer("ME2.chng")
the_input.append("$")
#print the_input
print "!!!"

#i wanna make a dictionary such that 
#the keys => the line number of a code, 
#the values => actual line of code
dict_of_line_and_code = {}
templist = []
count = 1


for j in the_input:
    if j != '\\n':
        templist.append(j)
    else:
        dict_of_line_and_code[count] = templist
        count += 1
        templist = []

the_keys = dict_of_line_and_code.keys()
the_values = dict_of_line_and_code.values()

list_of_maps = []
ultralist = []
print "AAAA"
for i in the_keys:
    if dict_of_line_and_code[i] != []:
        templist = [ dict_of_line_and_code[i][0], i]
    else:
        templist = ['', i]
    ultralist.append(templist)

for j in ultralist:
    if j[0] != '':

        for k in grammar_rules.keys():
            if grammar_rules[k][2] == j[0]:
                j[0] = grammar_rules[k][0]
                break

copy = []

for j in ultralist:
    if j[0] in ["Print", "Input", "InputPrompt", "Arithmetic", "ArithmeticBlock", "Break", "Continue", "VarDecSegment", "For", "While", "If", "Elif", "Else", "Function"]:
        copy.append(j)

print copy
print "!!"


stack = [0] #we want the stack to be inititally 0
stack_var_index = 0

print ["stack",   "input",   "action"]
#first, we find the intersection of the last element of stack list
intersection = '0'

ultralist = [] #para sa ultralist ng mga reduces
counter = 0
sendList = []
while (1):
    action = [] #this is the 'action' list where the shift/reduce functions are shown
    #print the_input
    input_var_index = find_index(the_input[0])
   
		#print counter
		
    try:
        intersection = lr_table[stack_var_index][input_var_index]
        #print [stack]
    except TypeError:
        #this is for inputs that are not what we declared in the rules
        print "Syntax Error."
        break
    else:
        if (intersection[0] == 's'): #if the order is a 'shift'
            action = [intersection]
            stack.append ( the_input.pop(0) )
            stack.append ( int(intersection[1:]) )
            stack_var_index = int(intersection[1:])

        elif (intersection[0] == 'r'):#if the order is a 'reduce'


            temp1 = grammar_rules[int(intersection[1:])] 
			#so pag rule 1, temp1 = ['A', '->', 'id', '=', 'E']


            index_arrow = temp1.index('->')
            

            temp2 = temp1[index_arrow + 1:]





            if "''" in temp2:
                temp2 = []
            """print "ddd"
            for i in temp2:
                print i
            print 'end'"""				
            count = len(temp2) * 2

            action = [intersection]
            #print [ stack ]
            #print [ the_input ]
            #print [ action ]            
            while (count != 0): #the popping process
                stack.pop()
                count -= 1
            last_num = stack[len(stack) - 1]
            the_letter = grammar_rules[ int(intersection[1:]) ][0]#append the LHS of the grammar rule
            
            stack.append(the_letter)
            stack.append( lr_table[last_num][ find_index(the_letter) ] )

            stack_var_index = lr_table[last_num][ find_index(the_letter) ]

        elif (intersection[0] == 'z'): #if the order is 'accept'
            action = ["accept"]
            #print [ stack ]
            #print [ the_input ]
            #print [ action ]            
            print "DONE!"
            print action
            break
        else:
            #it found an 'x', meaning there's an error
            #note that in the documentation, when it says "no intersection",
            #it means that the intersection is an 'x' in this code
            print "Syntax Error.!"
            break
        if the_input[0] == "\\n":
            counter = counter + 1
        print "--"
        #print [ stack ]
        #print "========================="
        #print [ the_input ]
        #print "========================="
        print [ action ]

