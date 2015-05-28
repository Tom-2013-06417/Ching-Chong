from parseTableConverter import parseTableMaker
from parseTableConverter import rules

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


list_of_tokens = []
list_of_tokens = raw_input("Input:") + '$'
the_input = []
i = 0
'''
for i in list_of_tokens: #this removes all the spaces in the input
    if (i != ' '):
        the_input.append(i)
'''


the_input=["Hi,Iam", "A", "a", "a", ".", "\n", "$"]

stack = [0] #we want the stack to be inititally 0
stack_var_index = 0

print ["stack",   "input",   "action"]
#first, we find the intersection of the last element of stack list
intersection = '0'

while (True):
    action = [] #this is the 'action' list where the shift/reduce functions are shown
    input_var_index = find_index(the_input[0])

    try:
        intersection = lr_table[stack_var_index][input_var_index]
    except TypeError:
        #this is for inputs that are not what we declared in the rules
        print "Syntax Error."
        break
    else:
        if (intersection[0] == 's'): #if the order is a 'shift'
            action = [intersection]
            print [ stack, the_input, action ]

            stack.append ( the_input.pop(0) )
            stack.append ( int(intersection[1:]) )
            stack_var_index = int(intersection[1:])

        elif (intersection[0] == 'r'):#if the order is a 'reduce'
            temp1 = grammar_rules[int(intersection[1:])] #so pag rule 1, temp1 = ['A', '->', 'id', '=', 'E']
            index_arrow = temp1.index('->')

            temp2 = temp1[index_arrow + 1:]
            count = len(temp2) * 2
            
            action = [intersection]
            print [ stack, the_input, action ]
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
            print [ stack, the_input, action ]
            break
        else:
            #it found an 'x', meaning there's an error
            #note that in the documentation, when it says "no intersection",
            #it means that the intersection is an 'x' in this code
            print "Syntax Error.!"
            break


        
        
        
    



