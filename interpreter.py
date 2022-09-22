from decimal import *
import os

valid_file = False
while valid_file == False:
    os.system('CLS')
    file_name = input("Select a valid .txt file to read:" )
    valid_file = os.path.exists(file_name)

file = open(file_name, "r")
code_to_read = file.read()
NUMBER = '0123456789'
OPERATOR = ['+','-','*','/']
PARENTHESIS = '()'
CONDITION = '|&'
INVALID_CHARS = '+*/);,.='
TRUE_AND_FALSE = [True, False]

# these will hold all values created by the Lexer
numbers = []
operators = []
l_parenthesis = []
r_parenthesis = []
conditions = []
strings = []
identifiers = []
comparison_assignment = []

index_of_words = []

# This will hold the text of the current line
curr_line = ''

# This will hold all lines separately
lines = []

# Is called when something goes wrong, will close the application.
def errorHandling(error):
    print(error)
    exit()

# Used to create single character token
def createNew(x, type):
    type.append(x)

# Used to create parenthesis token
def parenthesisManager(x):
    if x == '(':
        index_of_words.append([len(l_parenthesis),"("])
        l_parenthesis.append(x)
    if x == ')':
        index_of_words.append([len(r_parenthesis),")"])
        r_parenthesis.append(x)
    else:
        pass

# Used to create number token
def createNumber(index):
    temp = ''
    dot_count = 0
    count = 0

    for curr_char in code_to_read[index::]:
        if curr_char == ' ' or curr_char in OPERATOR or curr_char in CONDITION or curr_char in PARENTHESIS or curr_char == ';':
            index_of_words.append([len(numbers), "numbers"])
            try:
                converted_num = Decimal(temp)
            except:
                errorHandling(f'Could not create a number out of {temp}.')
            numbers.append(converted_num)
            return count -1
        elif curr_char == '.':
            dot_count +=1
            if dot_count > 1:
                errorHandling("Error creating number, too many dots.")
            curr_char
        elif curr_char == '"':
            errorHandling("Error creating number, if doing string operation, use operators.")
        temp += curr_char
        count +=1

    index_of_words.append([len(numbers), "numbers"])
    converted_num = Decimal(temp)
    numbers.append(converted_num)
    return count -1

# Used to create string token
def createString(index, curr_char):
    temp_string = ""
    for curr_char in code_to_read[index+1::]:
        if curr_char == '"':
            index_of_words.append([len(strings),"strings"])
            strings.append(temp_string)
            return len(temp_string)+1
        else:
            temp_string += curr_char

# Used to create comparison/assignment token
def createCA(index):

    index_of_words.append([len(comparison_assignment), "comparison_assignment"])
    temp = ""
    x = code_to_read[index::]
    if x[0] == '=':
        temp += x[0]
        if x[1] == '=':
            temp += x[1]
            comparison_assignment.append(temp)
            if x[2] == ';' or x[2] == '+' or x[2] == '/' or x[2] == '*' or x[2] == '=':
                errorHandling("Error creating '=='")
            return 1 # Successfully created '=='
        elif x[1] in INVALID_CHARS:
            errorHandling("# Error creating '='") 
        else:
            comparison_assignment.append(temp)
            return 0 # Successfully created '='

    elif x[0] == '>':
        temp += x[0]
        if x[1] == '=':
            temp += x[1]
            comparison_assignment.append(temp)
            if x[2] == ';' or x[2] == '+' or x[2] == '/' or x[2] == '*' or x[2] == '=' or x[2] == '<' or x[2] == '>':
                errorHandling("Error creating '>='")
            return 1 # Successfully created '>='
        elif x[1] in INVALID_CHARS:
            errorHandling("Error creating '>'")
        else:
            comparison_assignment.append(temp)
            return 0 # Successfully created '>'

    elif x[0] == '<':
        temp += x[0]
        if x[1] == '=':
            temp += x[1]
            comparison_assignment.append(temp)
            if x[2] == ';' or x[2] == '+' or x[2] == '/' or x[2] == '*' or x[2] == '=' or x[2] == '<' or x[2] == '>':
                errorHandling("Error creating '<='")
            return 1 # Successfully created '<='
        elif x[1] in INVALID_CHARS:
            errorHandling("Error creating '<'")
        else:
            comparison_assignment.append(temp)
            return 0 # Successfully created '<'

    elif x[0] == '!':
        temp += x[0]
        if x[1] == '=':
            temp += x[1]
            if x[2].isalpha() or x[2] == '(' or x[2] == ' ':
                comparison_assignment.append(temp)
                return 1 # Successfully created '!='
            else:
                errorHandling("Error creating '!='")
        elif x[1].isalpha() or x[1] == '(' or x[1] == ' ':
            comparison_assignment.append(temp)
            return 0 # Succesfully created '!'
        else:
            errorHandling("Error creating '!'")

# Used to create True and False tokens. Supports creation of variable/function name
def createIdentifier(index):
    temp = ""
    count = 0
    for curr_char in code_to_read[index::]:
        if curr_char == ' ' or curr_char in PARENTHESIS or curr_char in OPERATOR or curr_char == '=' or curr_char == ';':
            index_of_words.append([len(identifiers), "identifiers"])
            if temp == 'True':
                identifiers.append(True)
            elif temp == 'False':
                identifiers.append(False)
            else:
                identifiers.append(temp)
            return count -1
        elif curr_char.isalpha or curr_char in NUMBER:
            temp += curr_char
            count +=1
        else:
            errorHandling("Could not create identifier")

# Will segment the code to read inside parenthesis and pass to to the main function
# If no parenthesis exist, run only once
# Will loop until no more operations or parenthesis exist
def parser(list):
    parser_index = 0
    going_forward = True

    parserList = []
    parserIterator = 0
    while parserIterator < len(list):
        parserList.append(getValueOfWords(parserIterator))
        parserIterator += 1

    math_temp = []
    index_to_pop = []
    if list.count("(") != list.count(")"):
        errorHandling("Missing parenthesis.")

    while parserList.count('+') + parserList.count('-') + parserList.count('*') + parserList.count('/') + parserList.count('!') + parserList.count('==') + parserList.count('!=') + parserList.count('>') + parserList.count('>=') + parserList.count('<') + parserList.count('<=') + parserList.count('|') + parserList.count('&') > 0:
        if '(' in parserList:
            if parserList[parser_index] == ")" and going_forward == True:
                index_to_pop.append(parser_index)
                going_forward = False
                parser_index-=1
            elif parserList[parser_index] != ")" and going_forward == True:
                parser_index+=1
            elif parserList[parser_index] != "(" and going_forward == False:
                index_to_pop.append(parser_index)
                math_temp.append(parserList[parser_index])
                parser_index-=1
            elif parserList[parser_index] == "(" and going_forward == False:
                index_to_pop.append(parser_index)
                index_to_pop.reverse()
                math_temp.reverse()
                mainLoop_return = mainLoop(math_temp)
                mlr_index = 0
                while mlr_index < len(mainLoop_return):
                    parserList.insert(index_to_pop[0+mlr_index], mainLoop_return[mlr_index])
                    mlr_index += 1
                for pop in index_to_pop:
                    parserList.pop(index_to_pop[len(mainLoop_return)])
                going_forward = True
                mlr_index = 0
                index_to_pop.clear()
                math_temp.clear()
        else:
            parserList = mainLoop(parserList)

    return(parserList[0])

# Will iterate through passed values and do the necessary operations in order
# Check README for order
def mainLoop(op_and_num):
    pm_i = 0
    while pm_i < len(op_and_num):
        if op_and_num[pm_i] == '-' or op_and_num[pm_i] == '+':
            if pm_i == 0 and str(op_and_num[pm_i+1]).isdecimal():
                op_and_num[pm_i+1] = -op_and_num[pm_i+1]
                op_and_num.pop(0)
                pm_i = 0
            elif type(op_and_num[pm_i-1]) == Decimal and type(op_and_num[pm_i+1]) == Decimal:
                pass
            elif isinstance(op_and_num[pm_i-1], str) and isinstance(op_and_num[pm_i+1], str):
                pass
            elif str(op_and_num[pm_i+1]) in OPERATOR and type(op_and_num[pm_i+2]) == Decimal:
                if op_and_num[pm_i+1] == '+':
                    op_and_num[pm_i+1] = +op_and_num[pm_i+2]
                elif op_and_num[pm_i+1] == '-':
                    op_and_num[pm_i+1] = -op_and_num[pm_i+2]
                op_and_num.pop(pm_i+2)
                pm_i = 0
            else:
                errorHandling(f'Invalid operation: {op_and_num[pm_i]} {op_and_num[pm_i+1]}')
        pm_i+=1
    
    mathloop_index = 0
    dwmad = False
    while op_and_num.count('+') + op_and_num.count('-') + op_and_num.count('*') + op_and_num.count('/') > 0:
        if mathloop_index == len(op_and_num):
            dwmad = True
            mathloop_index=0
        elif op_and_num[mathloop_index] == '*' or op_and_num[mathloop_index] == '/':
            temp_num_to_insert = (handleMath(op_and_num[mathloop_index-1], op_and_num[mathloop_index+1], op_and_num[mathloop_index]))
            op_and_num.insert(mathloop_index-1, temp_num_to_insert)
            for i in range(3):
                op_and_num.pop(mathloop_index)
            mathloop_index=0
        elif dwmad == True:
            if op_and_num[mathloop_index] == '+' or op_and_num[mathloop_index] == '-':
                temp_num_to_insert = (handleMath(op_and_num[mathloop_index-1], op_and_num[mathloop_index+1], op_and_num[mathloop_index]))
                op_and_num.insert(mathloop_index-1, temp_num_to_insert)
                for i in range(3):
                    op_and_num.pop(mathloop_index)
                mathloop_index=0

        mathloop_index+=1

    ili = 0
    while '!' in op_and_num:
        try:
            if op_and_num[ili] == '!':
                try:   
                    if op_and_num[ili+1] == 'True':
                        op_and_num[ili+1] = 'False'
                    elif op_and_num[ili+1] == 'False':
                        op_and_num[ili+1] = 'True'
                    else:
                        errorHandling("Invalid syntax.")
                    op_and_num.pop(ili)
                except:
                    errorHandling("Error, end of file.")
                ili = 0
            else:
                ili += 1
        except:
            errorHandling("Something went wrong while handling inversion.")

    mci = 0
    while op_and_num.count('>') + op_and_num.count('>=') + op_and_num.count('<') + op_and_num.count('<=') > 0:
        try:
            if op_and_num[mci] == '>' or op_and_num[mci] == '>=' or op_and_num[mci] == '<' or op_and_num[mci] == '<=':
                try:
                    op_and_num[mci-1] = handleLogic(op_and_num[mci-1], op_and_num[mci+1], op_and_num[mci])
                    op_and_num.pop(mci)
                    op_and_num.pop(mci)
                except:
                    errorHandling("Error, end of file.")
                mci = 0
            else:
                mci += 1
        except:
            errorHandling("Something went wrong while handling math comparisons.")

    ci = 0
    while op_and_num.count('==') + op_and_num.count('!=')> 0:
        try:
            if op_and_num[ci] == '==' or op_and_num[ci] == '!=':
                try:
                    op_and_num[ci-1] = handleLogic(op_and_num[ci-1], op_and_num[ci+1], op_and_num[ci])
                    op_and_num.pop(ci)
                    op_and_num.pop(ci)
                except:
                    errorHandling("Error, end of file.")
                ci = 0
            else:
                ci += 1
        except:
            errorHandling("Something went wrong while handling comparisons.")

    aoi = 0
    dwa = False
    while op_and_num.count('|') + op_and_num.count('&')> 0:
        if op_and_num.count('&') == 0:
            dwa = True
        try:
            if op_and_num[aoi] == '&':
                op_and_num[aoi-1] = handleLogic(op_and_num[aoi-1], op_and_num[aoi+1], op_and_num[aoi])
                try:
                    op_and_num.pop(aoi)
                    op_and_num.pop(aoi)
                except:
                        errorHandling("Error, end of file.")
                aoi = 0
            elif op_and_num[aoi] == '|' and dwa:
                op_and_num[aoi-1] = handleLogic(op_and_num[aoi-1], op_and_num[aoi+1], op_and_num[aoi])
                try:
                    op_and_num.pop(aoi)
                    op_and_num.pop(aoi)
                except:
                    errorHandling("Error, end of file.")
                aoi = 0
            else:
                aoi += 1
        except:
            errorHandling("Something went wrong while handling comparisons.")

    return op_and_num

# Handles comparisons and returns True or False
def handleLogic(a, b, op):
    try:
        if op == '==':
            return a == b
        elif op == '!=':
            return a != b

        if type(a) != type(b):
                errorHandling(f'Cannot compare {a} and {b}')

        if op == '>':
            return a > b
        elif op == '>=':
            return a >= b
        elif op == '<':
            return a < b
        elif op == '<=':
            return a <= b
        
        if a in TRUE_AND_FALSE and b in TRUE_AND_FALSE:
            if op == '|':
                return a or b
            elif op == '&':
                return a and b
        else:
            errorHandling("Both values need to be of Boolean type.")
    except:
        print(f'{a} {op} {b}')
        errorHandling("Wrong logic syntax.")

# Handles math operations between 2 values
def handleMath(a, b, op):
    temp_value = Decimal(0)
    if op == '+':
        if type(a) != type(b):
            errorHandling(f'Cannot get sum of {a} and {b}')
        else:
            try:
                temp_value = a + b
            except:
                print(f'{a} {op} {b}')
                errorHandling("Wrong math syntax.")
    elif op == '-':
        if type(a) != type(b):
            errorHandling(f'Cannot get subtration of {a} and {b}')
        else:
            try:
                temp_value = a - b
            except:
                print(f'{a} {op} {b}')
                errorHandling("Wrong math syntax.")
    elif op == '*':
        if type(a) != type(b):
            errorHandling(f'Cannot get multiplication of {a} and {b}')
        else:
            try:
                temp_value = a * b
            except:
                print(f'{a} {op} {b}')
                errorHandling("Wrong math syntax.")
    elif op == '/':
        if type(a) != type(b):
            errorHandling(f'Cannot get division of {a} and {b}')
        else:
            try:
                temp_value = a / b
            except:
                print(f'{a} {op} {b}')
                errorHandling("Wrong math syntax.")
    return temp_value

# Returns value stored in global variables
def getValueOfWords(i):
    var = index_of_words[i]
    if var[1] == 'identifiers':
        return identifiers[var[0]]
    elif var[1] == 'numbers':
        return numbers[var[0]]
    elif var[1] == 'strings':
        return strings[var[0]]
    elif var[1] == 'operators':
        return operators[var[0]]
    elif var[1] == '(':
        return l_parenthesis[var[0]]
    elif var[1] == ')':
        return r_parenthesis[var[0]]
    elif var[1] == 'comparison_assignment':
        return comparison_assignment[var[0]]
    elif var[1] == 'conditions':
        return conditions[var[0]]

# Lexer
global_curr_char = 0
index = 0
while index < len(code_to_read):
    try:
        global_curr_char = code_to_read[index]
    except:
        print("No more code to read.")

    if global_curr_char in NUMBER:
        index += createNumber(index)
    elif global_curr_char in OPERATOR:
        index_of_words.append([len(operators), "operators"])
        createNew(global_curr_char, operators)
    elif global_curr_char in PARENTHESIS:
        parenthesisManager(global_curr_char)
    elif global_curr_char in CONDITION:
        index_of_words.append([len(conditions), "conditions"])
        createNew(global_curr_char, conditions)
    elif global_curr_char == '"':
        index += createString(index, global_curr_char)
    elif global_curr_char == '=' or global_curr_char == '>' or global_curr_char == '<' or global_curr_char == '!':
        index += createCA(index)
    elif global_curr_char.isalpha():
        index += createIdentifier(index)

    curr_line += global_curr_char

    if global_curr_char == ';':
        lines.append(curr_line)
        print(code_to_read)
        print(parser(index_of_words))
        input("Press any key to close.")
        
    index += 1