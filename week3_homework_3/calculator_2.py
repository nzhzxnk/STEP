# *** Homework3 ***
# Handle parentheses in mathmatical expressions.

# *** Read series ***
# Read the line from left to right. Separate into numbers and individual symbols('+','-','*','/','(',')').
# |line|: User inputs a mathmatical expression. 
# |index|: Order of characters in the line.
# /token/: return each result as a dict. ex) {key='type': value='PLUS'}
# /index/: After read, return the next index.
# Note: make the rule of the line. (= isn't need etc..)

import re
# Note: parentheses_count is global variable. Difine here.
parentheses_count = 0

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

# parentheses_count: A counter of parentheses (opening parenthesis -> +1 , closing parenthesis -> -1).
# Check the nesting level. Verify the corresponding opening and closing for each pair. Finally, count should be '0'
# The layer will be as follows.
#         ((a+b)*c)/(d+e)
# layer = 12   2  1 1   1
def read_opening(line, index):
    global parentheses_count
    parentheses_count += 1
    token = {'type': 'OPENING','layer':parentheses_count}
    return token, index + 1

def read_closing(line, index):
    global parentheses_count
    token = {'type': 'CLOSING','layer':parentheses_count}
    parentheses_count -= 1
    return token, index + 1

#  *** Tokenize ***
# Separate numbers and individual symbols from the line (Read series). Compile all tokens into a list in original order.
# |line|: User inputs a mathmatical expression. 
# token: a number or an individual symbol separated from the line. The type is dict. ex) {key:'type', value:'PLUS'}
# Insert dummy '(' and ')' in order to evaluate. The layer will be as follows.
#         (((a+b)*c)/(d+e))
# layer = 012   2  1 1   10
# /tokens/: return a list of all tokens. ex) [{'type':'OPENING','layer':'0'}, {'type':'NUMBER','number':'1'}, {'type':'PLUS'}, {'type':'NUMBER','number':'2'}...]
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
        elif line[index] == '(':
            (token, index) = read_opening(line, index)
        elif line[index] == ')':
            (token, index) = read_closing(line, index)
        else:
            # If an unexpected symbol exists in the line, the program will crash and display error code(1). 
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    # If there is a mismatch between the number of opening and closing parentheses, the program will crash and display error code(1). 
    if parentheses_count != 0:
        print('Parentheses mismatch error: Unbalanced parentheses: ' + line[index])
        exit(1)
    tokens.insert(0, {'type': 'OPENING','layer':0}) # Insert a dummy '(' token.
    tokens.append({'type':'CLOSING', 'layer':0}) # Insert a dummy ')' token.
    return tokens

#  *** Evaluate ***
# Evaluate the elements in a token list following steps.
# Step1) Evaluate from the first one of innermost parenthese. 
#        Innermost parenthese has the highest layer.
#        Search for the first parenthesis with highest layer. 
# Step2) prioritized_evaluate: Evaluate　multiplication and division as a priority. 
#        Within the scope between opening and its corresponding closing parenthesis.
# Step3) standard_evaluate: Evaluate　addition and subtraction.
#        Within the scope between opening and its corresponding closing parenthesis.
# Step4) Evaluate other parenthese. 
#        Search for the next parenthesis with highest layer.
# Step5) Repeat Step2-4 until the length of tokens become 1. Then this should be answer.
# |tokens|: a list of all tokens. ex) [{'type':'OPENING','layer':'0'}, {'type':'NUMBER','number':'1'}, {'type':'PLUS'}, {'type':'NUMBER','number':'2'}...]
# /tokens[0]['number']/: Ultimately the tokens list should contain only a single 'NUMBER' token. This is the answer of the line. 
def evaluate(tokens):
    is_prioritized_evaluating = False # Create flag for runnning prioritized_evaluate -> is_prioritized_evaluating
    is_standard_evaluating = False # Create flag for runnning standard_evaluate -> is_standard_evaluating
    # Store the index of opening parenthesis focusing on during prosessing.
    # Note: now_opening_index is immutable. Serve as a fixed reference point because processing doesn't affect elements before it.
    now_opening_index = -1 
    index = 0 # Note: index moves around.
    now_layer = max([token['layer'] for token in tokens if token['type'] == 'CLOSING']) # Store the highest layer at this point. 
    # print(f"now_layer={now_layer}") # Debag

    # *** Prioritized_evaluate ***
    # Evaluate　multiplication and division as a priority within the scope between opening and its corresponding closing parenthesis.
    # Each results overwrite the last token of each segments. 
    # The original 'NUMBER', 'ASTERISK' and 'SLASH' are replaced with empty dictionaries. ('{}') 
    # Remove empty dictionaries from tokens and add some other token to prepare for next standard_evaluate.
    # |tokens|: a list of all tokens. 
    # |index|: the index of token focusing on now.
    # |now_opening_index|: the index of opening parenthesis focusing on during prosessing
    # |now_layer|: the highest layer at this point.
    # /tokens/: Return a list of all tokens. The content is modified through calculation.
    def prioritized_evaluate(tokens,index,now_opening_index,now_layer):
        while True:
            if tokens[index]['type'] == 'ASTERISK': # If '*' exsists in the line, evaluate and put the result in tokens[index+1].
                if tokens[index - 1]['type'] == 'NUMBER' and tokens[index + 1]['type'] == 'NUMBER':
                    multi_ans = tokens[index-1]['number']*tokens[index+1]['number']
                    tokens[index - 1] = {} # Replace with empty dictionary.
                    tokens[index] = {} 
                    tokens[index + 1] = {'type':'NUMBER', 'number':multi_ans} # Results overwrite the last token. 
                else: # If an unexpected symbol exists in the line, the program is crashed and show errorcode(1). 
                    print('Invalid syntax around ASTERISK')
                    exit(1)
            elif tokens[index]['type'] == 'SLASH': # If '/' exsists in the line, evaluate and put the result in tokens[index+1].
                if tokens[index - 1]['type'] == 'NUMBER' and tokens[index + 1]['type'] == 'NUMBER':
                    div_ans = tokens[index-1]['number']/tokens[index+1]['number']
                    tokens[index - 1] = {}
                    tokens[index] = {}
                    tokens[index + 1] = {'type':'NUMBER', 'number':div_ans}
                else:
                    print('Invalid syntax around SLASH')
                    exit(1)
            # If corresponding closing exsists in the line, finish prioritized_evaluate and prepare for next standard_evaluate.
            elif tokens[index]['type'] == 'CLOSING' and tokens[index]['layer'] == now_layer:  
                tokens = [token for token in tokens if token] # Delete empty dicts.
                tokens[now_opening_index] = {'type':'NUMBER', 'number':0} # In standard_evaluate, the result will overwrite tokens[now_opening_index].
                if tokens[now_opening_index+1]['type'] == 'NUMBER':
                    tokens.insert(now_opening_index+1, {'type': 'PLUS'}) # Insert a dummy '+' token.
                elif tokens[now_opening_index+1]['type'] == 'MINUS':
                    pass
                else:
                    print('Invalid syntax around OPENING')
                    exit(1)
                return tokens
            index += 1 # Until find corresponding closing, continue prioritized_evaluate.
    
    # *** Stndard_evaluate ***
    # Evaluate　addition and subtraction within the scope between opening and its corresponding closing parenthesis.
    # The result overwrite tokens[now_opening_index] location. 
    # All other original tokens are replaced with empty dictionaries ('{}').
    # Remove empty dictionaries from tokens and prepare for searching for the next parenthesis.
    # |tokens|: a list of all tokens. 
    # |index|: the index of token focusing on now.
    # |now_opening_index|: the index of opening parenthesis focusing on during prosessing
    # |now_layer|: the highest layer at this point.
    # /tokens/: Return a list of all tokens. The content is modified through calculation.
    def standard_evaluate(tokens,index,now_opening_index,now_layer):
        last_is_number = False
        while True:
            if tokens[index]['type'] == 'NUMBER':
                last_is_number = True
                if tokens[index - 1]['type'] == 'PLUS': # If the previous operator is '+', tokens[index]['number'] add result.
                    tokens[now_opening_index]['number'] += tokens[index]['number']
                    tokens[index-1] = {}
                    tokens[index] = {}
                elif tokens[index - 1]['type'] == 'MINUS': # If the previous operator is '-', tokens[index]['number'] subtract from result.
                    tokens[now_opening_index]['number'] -= tokens[index]['number']
                    tokens[index-1] = {}
                    tokens[index] = {}
                else: # If an unexpected symbol exists in the line, the program is crashed and show errorcode(1). 
                    print('Invalid syntax around NUMBER')
                    exit(1)
            elif tokens[index]['type'] == 'CLOSING' and tokens[index]['layer'] == now_layer:
                tokens[index] = {} # Closing parenthesis replace with empty dict.
                tokens = [token for token in tokens if token] # Delete empty dicts.
                if last_is_number:
                    return tokens
                else:
                    print('Invalid syntax around CLOSING')
                    exit(1)
            else:
                last_is_number = False
                
            index += 1 # Until find corresponding closing, continue prioritized_evaluate.
    
    while len(tokens) > 1 and index < len(tokens): # Ultimately the tokens list should contain only a single 'NUMBER' token.
        # print(f"tokens={tokens}") # Debag
        if tokens[index]['type'] == 'OPENING' and tokens[index]['layer'] == now_layer: # If find the first opening parenthesis with highest layer, repeat Step2-4. 
            is_prioritized_evaluating = True # Start prioritized_evaluate from now_opening_index.
            now_opening_index = index
            index += 1 
        if not is_prioritized_evaluating and not is_standard_evaluating: # If both is_prioritized_evaluating and is_standard_evaluating is False, move next!!!
            index += 1
        if is_prioritized_evaluating:
            tokens = prioritized_evaluate(tokens,index,now_opening_index,now_layer)
            index = now_opening_index+1 # Start standard_evaluate from the next of now_opening_index.
            is_prioritized_evaluating = False # Finish prioritized_evaluate.
            is_standard_evaluating = True
            # print(f"tokens={tokens}") # Debag
        if is_standard_evaluating:
            tokens = standard_evaluate(tokens,index,now_opening_index,now_layer)
            index = 0 # Start searching for the next parenthesis.
            is_standard_evaluating = False # Finish standard_evaluate.
            # print(f"tokens={tokens}") # Debag
            # print(any(token['type'] == 'CLOSING' for token in tokens)) # Debag
            if any(token['type'] == 'CLOSING' for token in tokens):
                now_layer = max([token['layer'] for token in tokens if token['type'] == 'CLOSING']) # Update the highest layer at this point. 
            # print(f"now_layer={now_layer}") # Debag
    return tokens[0]['number'] 

# *** Test ***
def test(line):
    line = re.sub(r'\s+', '', line) # Remove space
    tokens = tokenize(line)
    # print(f"tokens={tokens}") # Debag
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
    test("(-1)+2")
    test("-1+2")
    test("2+(-1)")
    test("2-1")
    test("3-(-4.44)")
    test("(-4.44)-3")
    test("-4.44-3")
    test("2*(-3)")
    test("(-2)*3")
    test("-2*3")
    test("(-2)*(-3)")
    test("(-2.222)*3")
    test("4/(-5)")
    test("(-4)/5")
    test("-4/5")
    test("(-4)/(-5)")
    test("4/(-5.5555)")
    # *** Basic include parentheses ***
    test("1+2-3")
    test("(1+2)-3")
    test("1+(2-3)")
    test("1.1+2-3.333")
    test("(1.1+2)-3.333")
    test("1.1+(2-3.333)")
    test("4/2*3")
    test("(4/2)*3")
    test("4/(2*3)")
    test("4/2.22*3.333")
    test("(4/2.22)*3.333")
    test("4/(2.22*3.333)")
    # *** Advanced ***
    test("10000+1000-100+10-1+0.1-0.01+0.001-0.0001")
    test("-10000+1000-(-100)+10-1+(-0.1)-0.01+0.001-(-0.0001)")
    test("9*8.7/6.54*3.2/2")
    test("9*(-8.7/6.54)*(-3.2)/2")
    test("-21/11+10-1.2*1.23+1.234-1.2345/1.23456+1.234567*1.2345678-1.23456789")
    test("-21/((11+10)*(1.2-1.23/(1.234*(1.2345-1.23456)+1.234567)*1.2345678)-1.23456789)")
    # *** Invaild input (OK) ***
    test("1 + 2　")
    test("1")
    test("-2")
    test("(-3)")
    test("(-(-4))")
    # # *** Invaild input (NG) ***
    # test("001")
    # test("1+1あ”％？1*1-1")  # Expected to display 'Invalid character found: '
    # test("1+a")  # Expected to display 'Invalid character found: '
    # test("1.2.3456+7")  # Expected to display 'Invalid character found: '
    # test("(1+2)+3)") # Expected to display 'Parentheses mismatch error: Unbalanced parentheses: '
    # test("((1+2)+3") # Expected to display 'Parentheses mismatch error: Unbalanced parentheses: '
    # test("(1+()2)+3") # Expected to display 'Invalid syntax'
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
    # # *** Undifined (NG) ***___
    # test("3+1//2")  # Expected to display 'Invalid syntax'
    # test("3+1**2")  # Expected to display 'Invalid syntax'
    print("==== Test finished! ====\n")

run_test()

# *** Main code of this program ***
while True:
    print('>', end="")
    line = re.sub(r'\s+', '', input()) # Remove space
    tokens = tokenize(line)
    answer = evaluate(tokens)
    # Note: print("answer = %f\n" % answer) == print(f"answer = {answer}\n")
    print("answer = %f\n" % answer)
