import re
identifiers = '[_a-zA-Z][_a-zA-Z0-9]*'
integers = '[0-9][0-9]*'
float_val = '\d+\.\d*'
float_val1 = '\.\d+'
octal = '[0][0-7]{1,2}'
hexadecimal = '[0][x][0-9a-fA-f]{1,2}'
operations = {'=':'assign_op', '+':'add_op', '-':'sub_op', '*':'mul_op', '/':'div_op', '%':'mod_op', '\'':'single_quotes', '"':'double_quotes',
             '(':'left_paranthesis',')':'right_paranthesis', ';':'delimiter','{':'left_curly','}':'right_curly', '>':"GREATER_THAN",
              '<':"LESS_THAN", "!":"EXCLAMATION", ":":"EACH"}

keywords = {'double':'DOUBLE_CODE','float':'FLOAT_CODE','int':"INT_CODE"
            ,'break':"BREAK_CODE",'continue':'CONTINUE_CODE',
            'else':'ELSE_CODE','for':'FOR_CODE','long':'LONG_CODE','switch':'SWITCH_CODE','void':'VOID_CODE',
            'case':'CASE_CODE','default':'DEFAULT_CODE','register':'REGISTER_CODE','sizeof':'SIZEOF_CODE',
            'char':'CHAR_CODE','do':'DO_CODE','extern':"EXTERN_CODE",'if':'IF_CODE','return':'RETURN_CODE',
            'static':'STATIC_CODE','while':'WHILE_CODE', 'main':'MAIN_CODE', 'forEach':'FOREACH_CODE'}

delimiter = ';'
parsed_array = []
val_temp=''

# C
# lex() = getNext()
# <stmt> → <while> | <do-while> | <if> | <foreach> | <for> | <assignment> | <return>
# <Expression> → <Expression> + <Term> | <Expression> - <Term> | <Term>
# <Term> → <Term> * <Factor> | <Term> / Factor | <Term> % <Factor> | <Factor> 
# <Factor> →  Identifier | float | int | double

# <bool> → ‘IDENTIFIER’ (  ‘==’ | ‘!=’ | ‘<=’ | ‘>=’ | ‘<’ | ‘>’ ) ‘IDENTIFIER’ 

with open('raw_data.txt','r') as file:
    while True:
        new_char = file.read(1)
        if new_char=="":
            break
        token = new_char
        identifier = re.fullmatch(identifiers, new_char)
        if identifier:
            val='IDENTIFIER'
        integer = re.fullmatch(integers, new_char)
        floats = re.fullmatch(float_val, new_char)
        if integer:
            val='INTEGER'
        if new_char == ".":
            while new_char!='':
                next_char = file.read(1)
                if next_char == "":
                    break
                if next_char == " ":
                    break
                temp_char = token + next_char
                float_dot = re.fullmatch(float_val1, temp_char)
                if float_dot:
                    token = temp_char
                    val = "FLOAT" 
                if next_char in operations.keys():
                    val_temp = operations[next_char]  
                else:
                    break
        if new_char!="" and new_char in operations.keys():
            val = operations[new_char]
            parsed_array.append((new_char, val))              
        while new_char!='' and identifier: 
            next_char = file.read(1)
            if next_char == "":
                break
            if next_char == " ":
                break
            temp_char = token + next_char
            identifier = re.fullmatch(identifiers, temp_char)
            if identifier:
                token = temp_char
                val="IDENTIFIER"
            if next_char in operations.keys():
                val_temp = operations[next_char]   
        while new_char!='' and integer or floats:
            next_char = file.read(1)
            if next_char == "":
                break
            if next_char == " ":
                break
            temp_char = token + next_char
            integer = re.fullmatch(integers, temp_char)
            floats = re.fullmatch(float_val, temp_char)
            if floats:
                token = temp_char
                val = "FLOAT"
            elif integer:
                token = temp_char
                val="INTEGER"
            if next_char in operations.keys():
                val_temp = operations[next_char]
        
        if val == "IDENTIFIER" or val == "INTEGER" or val=="FLOAT" or val=="OCTAL"and token != " " and token != "\n":
            if token != " ":
                parsed_array.append((token,val))
            token=''
            val=""
        if val_temp and next_char != " " and next_char != "\n":
            parsed_array.append((next_char, val_temp))
            val_temp=''
        token=''
        val=""
        if new_char=="":
            break 

#checks if identifier is a keyword and then replaces identifier with the keyword
for i in range(len(parsed_array)):
    if parsed_array[i][1] == 'IDENTIFIER':
        if parsed_array[i][0] in keywords.keys():
            temp_var = list([parsed_array[i][0],keywords[parsed_array[i][0]]])
            parsed_array[i] = tuple(temp_var)
i = 0
while i < len(parsed_array):
    if parsed_array[i][0] == "=" and parsed_array[i+1][0] == "=":
        parsed_array.pop(i+1)
        parsed_array[i] = ("==", 'EQUALITY_OPERATOR')
    else:
        i +=1
i = 0
while i < len(parsed_array):
    if parsed_array[i][0] == ">" and parsed_array[i+1][0] == "=":
        parsed_array.pop(i+1)
        parsed_array[i] = (">=", 'GREAT_EQUAL')
    else:
        i +=1
i = 0
while i < len(parsed_array):
    if parsed_array[i][0] == "<" and parsed_array[i+1][0] == "=":
        parsed_array.pop(i+1)
        parsed_array[i] = ("<=", 'LESS_EQUAL')
    else:
        i +=1
i = 0
while i < len(parsed_array):
    if parsed_array[i][0] == "!" and parsed_array[i+1][0] == "=":
        parsed_array.pop(i+1)
        parsed_array[i] = ("!=", 'NOT_EQUAL')
    else:
        i +=1
for i in parsed_array:
    print(i)


def lex():
    global nextToken
    if parsed_array:
        val = parsed_array.pop(0)
        val = val[1]
        nextToken = val
        print(nextToken)
    else:
        nextToken = None

# <stmt> --> <if_stmt>|<while_stmt>|<for_stmt>|<forEach_stmt>|<assignment_stmt>|<return_stmt>|<do_while_stmt>|<switch_stmt>
def stmt():
    lex()
    if nextToken == 'INT_CODE' or nextToken == 'FLOAT_CODE' or nextToken == 'DOUBLE_CODE' or nextToken=='IDENTIFIER':
        assignment_stmt()
    elif nextToken == 'WHILE_CODE':
        while_stmt()
    elif nextToken == 'FOR_CODE':
        for_stmt()
    elif nextToken == 'IF_CODE':
        if_stmt()
    elif nextToken == 'RETURN_CODE':
        return_stmt()
    elif nextToken == 'FOREACH_CODE':
        forEach_stmt()
    elif nextToken == 'DO_CODE':
        do_while_stmt()
    elif nextToken == 'left_curly':
        block()

# <block> → ‘{‘  ( ‘ ‘ |  <stmt>  )  ‘}’
def block():
    print("Start <block>")
    if nextToken != 'left_curly':
        error()
    while nextToken != 'right_curly' and parsed_array:
        stmt()
    if nextToken == 'right_curly':
        print("END <block>")
    else:
        error()
        
# <assignment> → ‘int|float|double’ ‘IDENTIFIER’ ‘;’ |  ‘int|float|double’ ‘IDENTIFIER’  ‘=’ ‘IDENTIFIER’  ‘delimiter’ 
def assignment_stmt():
    print('Enter <assign statement>')
    if nextToken == 'INT_CODE' or nextToken == 'FLOAT_CODE' or nextToken=='DOUBLE_CODE':
        lex()
        if nextToken != 'IDENTIFIER':
            error()
        lex()
        if nextToken == 'assign_op':
            lex()
            expr()
            if nextToken != 'delimiter':
                error()
            print('End <assignement statement>')
        elif nextToken == "delimiter":
            print('END <assignment statement>')
        else:
            error()
    elif nextToken == 'IDENTIFIER':
        lex()
        if nextToken == 'assign_op':
            lex()
            expr()
            if nextToken != 'delimiter':
                error()
            print('End <assignement statement>')
        else:
            error()

    else:
        error()

# <Expression> → <Expression> + <Term> | <Expression> - <Term> | <Term>
def expr():
    print("Enter <expr>")
    term()
    while (nextToken == 'add_op' or nextToken == 'sub_op'):
        lex()
        term()
    print("Exit <expr>")
    
# <Term> → <Term> * <Factor> | <Term> / Factor | <Term> % <Factor> | <Factor> 
def term():
    print("Enter <term>")
    factor()

    while(nextToken == 'mult_op' or nextToken == 'div_op' or nextToken == 'mod_op'):
        lex()
        factor()
    print("Exit <term>")
    
# <Factor> →  Identifier | float | int 
def factor():
    print("Enter <factor>")
    if (nextToken == 'IDENTIFIER' or nextToken == 'INTEGER' or nextToken == 'FLOAT'):
        lex()

    elif nextToken == 'left_paranthesis':
        lex()
        expr()
        if nextToken == 'right_paranthesis':
            lex()
        else:
            error()
    else:
        error()
    print("Exit <factor>")


def bool_expr():
    print("Enter <bool_expr>")
    expr()
    if nextToken == "EQUALITY_OPERATOR" or nextToken == "NOT_EQUAL" or nextToken == "GREAT_EQUAL" or nextToken =="LESS_EQUAL" or nextToken == "GREATER_THAN" or nextToken == "LESS_THAN":
        lex()
        expr()
    else:
        error()
    print("End <bool_expr>")
    

def error():
    print("Error!")
    exit()

# <if> → ‘if’ ‘(‘ <bool_expr> ‘)’ <block> [else (<block>|<stmt>)]
def if_stmt():
    print("Enter <IF STMT>")
    if (nextToken != 'IF_CODE'):
        error()
    else:
        lex()
        if (nextToken != 'left_paranthesis'):
            error()
        else:
            lex()
            bool_expr()
            if nextToken != 'right_paranthesis':
                error()
            else:
                stmt()
                lex()
                if nextToken == 'ELSE_CODE':
                    print("ENTER <ELSE STMT>")
                    stmt()
                    print("EXIT <ELSE STMT>")
    print("End <IF STMT>")

# <for> → ‘for’ ‘(‘ (‘int| double| float’ | ‘int| double| float’ ‘IDENTIFIER’| ‘int| double| float’ ‘IDENTIFIER’ ‘=’ ‘IDENTIFIER’ | ‘IDENTIFIER’ | ‘ ’ ) ‘delimiter’ (‘IDENTIFIER’ ‘< | > | = | <=| >=’| == | !=’  ‘int|float|double’ | ‘IDENTIFIER’ |  int|float|double | ‘ ‘ ) ‘delimiter’ (‘ ‘ | int|float|double | ‘IDENTIFIER’ ‘(++|--)’) ‘)’ ‘<block>
def for_stmt():
    print("Enter <FOR STATMENT>")
    if nextToken != 'FOR_CODE':
        error()
    lex()
    if nextToken!='left_paranthesis':
        error()
    while nextToken != 'delimiter' and parsed_array:
        lex()
    if nextToken != 'delimiter':
        error()
    lex()
    while nextToken != 'delimiter' and parsed_array:
        lex()
    if nextToken != 'delimiter':
        error()
    while nextToken != 'right_paranthesis' and parsed_array:
        lex()
    if nextToken != 'right_paranthesis':
        error()
    stmt()
    print("End <for statement>") 

# <foreach> → ‘foreach’ ‘(‘ ‘IDENTIFIER’ ‘: ‘’IDENTIFIER’ ‘)’  <block>
def forEach_stmt():
    print("Enter <forEach statement>")
    if nextToken != "FOREACH_CODE":
        error()
    lex()
    if nextToken != 'left_paranthesis':
        error()
    lex()
    if nextToken != 'IDENTIFIER':
        error()
    lex()
    if nextToken != 'EACH':
        error()
    lex()
    if nextToken != 'IDENTIFIER':
        error()
    lex()
    if nextToken != 'right_paranthesis':
        error()
    else:
        stmt()
    print('End <forEach statement>')

# <while> → ‘while’ ‘(‘ <bool> ‘)’ <block>
def while_stmt():
    print('Enter <while statement>')
    if nextToken != 'WHILE_CODE':
        error()
    else:
        lex()
        if nextToken != 'left_paranthesis':
            error()
        else:
            lex()
            bool_expr()
            if nextToken != 'right_paranthesis':
                error()
            else:
                stmt()
    print("End <while statement>")

# <switch> → ‘switch’ ‘(‘ ‘)’ ‘{‘ ‘case <expr> : <stmt>’ | ‘default’ : <stmt> ‘}’
def switch_stmt():
    print('Enter <switch statement>')
    if nextToken != 'SWITCH_CODE':
        error()
    else:
        lex()
        if nextToken != 'left_paranthesis':
            error()
        lex()
        if nextToken != 'right_paranthesis':
            error()
        lex()
        if nextToken != 'left_curly':
            error()
        lex()
        if nextToken == 'CASE_CODE' or nextToken == 'DEFAULT_CODE':
            stmt()
        else:
            if nextToken != 'right_curly':
                error()
        print('End <switch statement>')

# <return> → ‘return’ (<assignment> | ‘IDENTIFIER’ ‘delimiter’)  
def return_stmt():
    print("Enter <Return statement>")
    if nextToken != 'RETURN_CODE':
        error()
    lex()
    expr()
    print('End <return statement>')

# <do-while> → ‘do’ <block> ‘while’ ‘(‘ <bool> ‘)’ ‘;’ 
def do_while_stmt():
    print('Enter <Do While Statement>')
    if nextToken != 'DO_CODE':
        error()
    stmt()
    lex()
    if nextToken != "WHILE_CODE":
        error()
    lex()
    if nextToken != "left_paranthesis":
        error()
    lex()
    bool_expr()
    if nextToken != 'right_paranthesis':
        error()
    lex()
    if nextToken != 'delimiter':
        error()
    print("End <Do While Statement>")

def program():
    print('START <Program>')
    lex()
    if nextToken != 'VOID_CODE':
        error()
    lex()
    if nextToken != 'MAIN_CODE':
        error()
    lex()
    if nextToken != 'left_paranthesis':
        error()
    lex()
    if nextToken != 'right_paranthesis':
        error()
    else:
        stmt()
    print('END <Program>')                 

#starts cheking the syntax of the program        
program()