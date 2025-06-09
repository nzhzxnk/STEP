# *** Homework 1 ***
# Add functions of multiplication and division.
# Note: Be mindful of modularization principles.
# Note: Be mindful of debaging principles.
# *** Homework 2 ***
# Add test cases.
# Note: Divise comprehensive test cases.

# *** Read series ***
# Read the line from left to right. Separate into numbers and individual symbols('+','-','*','/').
# |line|: User inputs a mathmatical expression. 
# |index|: Order of characters in the line.
# /token/: return each result as a dict. ex) {key='type': value='PLUS'}
# /index/: After read, return the next index.
# Note: make the rule of the line. (= isn't need etc..)

import re

def read_number(line, index):
    number = 0
    # *** Integral part *** 
    while index < len(line) and line[index].isdigit(): # isdigit(): the line consists only of numbers -> True, else -> False.
        number = number * 10 + int(line[index])
        index += 1
    # *** Dicimal part ***
    if index < len(line) and line[index] == '.': # If the character is '.' (comma), move to the next index.
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index

def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_asterisk(line, index):
    token = {'type': 'ASTERISK'}
    return token, index + 1

def read_slash(line, index):
    token = {'type': 'SLASH'}
    return token, index + 1

#  *** Tokenize ***
# Separate numbers and individual symbols from the line (Read series). Compile all tokens into a list in original order.
# |line|: User inputs a mathmatical expression. 
# token: a number or an individual symbol separated from the line. The type is dict. ex) {key:'type', value:'PLUS'}
# /tokens/: return a list of all tokens. ex) [{'type':'NUMBER','number':'1'}, {'type':'PLUS'}, {'type':'NUMBER','number':'2'}]
# Note: Read series contains a function to advance the index.
def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_asterisk(line, index)
        elif line[index] == '/':
            (token, index) = read_slash(line, index)
        else:
            # If an unexpected symbol exists in the line, the program will crash and display error code(1). 
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

#  *** Evaluate ***
# Evaluate the elements in a token list. Execute multiplication and division first, followed by other operation.
# |tokens|: a list of all tokens. ex) [{'type':'NUMBER','number':'1'}, {'type':'PLUS'}, {'type':'NUMBER','number':'2'}]
# /answer/: the answer of the line.
def evaluate(tokens):
    # *** Prioritized evaluate (for '*' and '/') ***
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'ASTERISK': # If '*' exsists in the line, evaluate and put the result in tokens[index+1].
            if tokens[index - 1]['type'] == 'NUMBER' and tokens[index + 1]['type'] == 'NUMBER':
                multi_ans = tokens[index-1]['number']*tokens[index+1]['number']
                tokens[index - 1] = {}
                tokens[index] = {}
                tokens[index + 1] = {'type':'NUMBER', 'number':multi_ans}
            else: # If an unexpected symbol exists in the line, the program is crashed and show errorcode(1). 
                print('Invalid syntax')
                exit(1)
        elif tokens[index]['type'] == 'SLASH': # If '/' exsists in the line, evaluate and put the result in tokens[index+1].
            if tokens[index - 1]['type'] == 'NUMBER' and tokens[index + 1]['type'] == 'NUMBER':
                div_ans = tokens[index-1]['number']/tokens[index+1]['number']
                tokens[index - 1] = {}
                tokens[index] = {}
                tokens[index + 1] = {'type':'NUMBER', 'number':div_ans}
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    
    # *** Evaluate other (for '+' and '-') ***
    answer = 0
    index = 0
    last_is_number = False
    # *** Remake tokens ***
    tokens = [token for token in tokens if token] # Delete empty dicts.
    if tokens[index]['type'] == 'NUMBER':
        tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token.
    elif tokens[index]['type'] == 'MINUS':
        pass
    else:
        print('Invalid syntax')
        exit(1)
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            last_is_number = True
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        else:
            last_is_number = False
        index += 1
    if last_is_number:
        return answer
    else:
        print('Invalid syntax')
        exit(1)

# *** Test ***
def test(line):
    line = re.sub(r'\s+', '', line)
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    # eval(): Interpret line as python-code, and evaluate this.
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))

# Note: Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    # *** Basic ***
    test("1+2")
    test("1.11+2")
    test("1.1+2.2222")
    test("3-4")
    test("5.55-4")
    test("3-4.44")
    test("3.3-4.4444")
    test("3.3333-4.4")
    test("3.3-3.3000")
    test("2*3")
    test("2.22*3")
    test("2.2*3.3333")
    test("4*0")
    test("4/5")
    test("4.44/5")
    test("4/5.55")
    test("4.4/5.5555")
    test("4.4444/5.5")
    test("4/1")
    # *** Negative number ***
    test("-1+2")
    test("-4.44-3")
    test("-2*3.33")
    test("-4/5")
    # *** Advanced ***
    test("10000+1000-100+10-1+0.1-0.01+0.001-0.0001")
    test("9*8.7/6.54*3.2/2")
    test("-21/11+10-1.2*1.23+1.234-1.2345/1.23456+1.234567*1.2345678-1.23456789")
    # *** Invaild input (OK)***
    test("1 + 2　")
    test("1")
    test("-2")
     # *** Invaild input (NG)***
    # test("001") # Expected to display 'SyntaxError: leading zeros in decimal integer literals are not permitted; use an 0o prefix for octal integers'
    # test("1+1あ”％？1*1-1")  # Expected to display 'Invalid character found: '
    # test("1+a")  # Expected to display 'Invalid character found: '
    # test("1.2.3456+7")  # Expected to display 'Invalid character found: '
    # test("1+2=") # Expected to display 'Invalid character found: '
    # test('*') # Expected to display 'Invalid syntax'
    # test("1+") # Expected to display 'Invalid syntax'
    # test("+1") # Expected to display 'Invalid syntax'
    # test("1-") # Expected to display 'Invalid syntax'
    # test("*2") # Expected to display 'Invalid syntax'
    # test("2*") # Expected to display 'Invalid syntax'
    # test("/2") # Expected to display 'Invalid syntax'
    # test("2/") # Expected to display 'Invalid syntax'
    # test("1/0") # Expected to display 'Invalid syntax'
    # test("3+1+-2")  # Expected to display 'Invalid syntax'
    # test("3+1-*2")  # Expected to display 'Invalid syntax'
    # # *** Undifined (NG)***___
    # test("3+1//2")  # Expected to display 'Invalid syntax'
    # test("3+1**2")  # Expected to display 'Invalid syntax'
    print("==== Test finished! ====\n")
run_test()

while True:
    print('> ', end="")
    line = re.sub(r'\s+', '', input())
    tokens = tokenize(line)
    answer = evaluate(tokens)
    # Note: print("answer = %f\n" % answer) == print(f"answer = {answer}\n")
    print("answer = %f\n" % answer)
