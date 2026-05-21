
# REDO <--- highlight this to check things to do

def parser(lexemes):
    from datetime import datetime
    #from compilerMain import append_log

    def append_log(input, logdate=False, logtime=True):
        if logtime:
            with open('log.txt', 'a') as log: log.write(f"{str(datetime.now().time())}:  ")

        with open('log.txt', 'a') as log: log.write(input)
        
        if logdate: 
            with open('log.txt', 'a') as log: log.write(str(datetime.now().date()))


    pos = 0

    open_block_char = '{'
    close_block_char = '}'

    defined_functions = ['print','input','get'] # script-defined functions are also added here
    defined_variables = []

    def peek():
        return lexemes[pos] if pos < len(lexemes) else None

    def consume(expected=None):
        nonlocal pos
        token = peek()
        if expected and token != expected:
            raise SyntaxError(f"Expected {expected}, got {token}")
        pos += 1
        return token
    
    def capitalize_if_true_false(value):
        value = {'true': 'True', 'false': 'False'}.get(value,value) # defaults to original value if not in table
        return value
    
    def get_arguements():
        arguements = []
        arguement = ''
        while peek() != ')': # arguement loop
            arguement += consume()
            if peek() == ',': 
                consume(',')
                arguements.append(arguement)
                arguement = ''

        arguements.append(arguement)
        return arguements
    
    
    def parse_block():
        """Consumes tokens until a closing character is found is found."""
        consume(open_block_char)
        block_statements = []

        while peek() != close_block_char and peek() is not None:
            # Recursively parse statements inside the block
            block_statements.append(parse_statement())

        if peek() != close_block_char: raise SyntaxError(f"Expected close block character '{close_block_char}' after block.")
        consume(close_block_char)
        return block_statements
    

    def parse_expression(name=consume(), line_end_chars=['\n', ';']):
        
        # function calls
        if peek() == '(':
            if name not in defined_functions: raise ReferenceError(f"{name} is not a defined function.")
            consume('(')
            arguements = get_arguements()

            if peek() != ')': raise SyntaxError("Expected bracket ')' after Function arguements.")
            consume(')')
            print(arguements)
            if peek() not in line_end_chars: raise SyntaxError(f"Expected line-ending character after FunctionStatement ({line_end_chars})...")
            consume()
            return {'type': 'FunctionCall', 'name': name, 'arguements': arguements}
        
        
        # table and list expression
        elif name in ['[','{',]:
            bracket_type = consume()
            close_bracket_type = {'[':']','{':'}',}.get(bracket_type)
            body = []
            while peek() != close_bracket_type: body.append(consume())
            consume(close_bracket_type)

            if peek() not in line_end_chars: raise SyntaxError(f"Expected line-ending character after FunctionStatement ({line_end_chars})...")
            consume()
            return {'type': {'[': 'ListExpression', '{': 'TableExpression'}.get(bracket_type), 'body': body}
        
        
        # math expression
        elif peek() in ['+','-','/','*']:
            operator = consume()
            quotient = parse_expression() # REDO variable name (quotient is for devision only so it dont fit)

            return {'type': 'MathExpression', 'operand': name, 'operator': operator, 'quotient': quotient}
        
        else:
            expression = name
            while peek() not in [line_end_chars, '=','.']: expression += consume()
            if peek() == '.': 
                consume('.')
                attribute = parse_expression()
                if attribute['type'] == 'FunctionCall':
                    return {'type': 'VariableExpression', 'Expression': expression, 'Attribute': attribute}
                
                else: raise TypeError(f"Expected FunctionCall type as attribute for variable {expression}") # REDO

            return {'type': 'Expression', 'Expression': expression, 'Attribute': None}

    
    
    # Recursively parse statements inside the block

    def parse_statement():
        passed = False
        if passed:
            last_token = token

        token = peek()

        line_end_chars = [';','\n']

        passed = True # not before first token

        if token == '\n': log = False
        else: log = True
        if log: append_log(f"Parsing token {token}...   ")

        # comment
        if token == '/':
            #print('comment2')
            if lexemes[pos + 1] == '/': # // comment
                consume('/'); consume('/')
                while peek() != '\n': # breaks on new line
                    consume()

            elif lexemes[pos + 1] == '*': # /* comment */
                consume('/'); consume('*')
                while peek() != '*' and lexemes[pos + 1] != '/': # breaks on */
                    consume()
                consume('*'); consume('/')

        # define function
        elif token == 'func':
            consume('func')
            name = consume()
            if peek() != '(': raise SyntaxError("Expected bracket '(' after defined function name.")
            consume('(')
            arguements = []
            while peek() != ')': # arguement loop
                arguements.append(consume())
                if peek() == ',': consume(',')

                else: break

            else: arguements = ''

            if peek() != ')': raise SyntaxError("Expected bracket ')' after function arguements.")
            consume(')')
            if peek() == open_block_char: body = parse_block() # if it sees an open block char '[' it'll parse the block

            else: body = [consume()]

            if peek() not in line_end_chars: raise SyntaxError(f"Expected line-ending character ({line_end_chars})...")
            consume()

            defined_functions.append[name] # add to list of already defined functions, for debugging with calling an undefined function
            return {'type': 'FunctionDefineStatement', 'name': name, 'arguements': arguements, 'body': body}

    # IF STUFF
        # if
        elif token == 'if':
            consume('if')
            condition = ''
            while peek() not in [open_block_char, ':']: condition += consume()

            if '=' in condition and '==' not in condition: raise SyntaxError(f"Expected boolean operator, got '='. (did you mean to use '=='?)")
            
            condition = capitalize_if_true_false(condition)
            if peek() == open_block_char: body = parse_block() # if it sees an open block char (often '{' or '[') it'll parse the block
            
            elif peek() == ':': 
                consume(':')
                body = [parse_statement()]
                

            if peek() not in line_end_chars: raise SyntaxError(f"Expected line-ending character ({line_end_chars})...")
            consume()

            return {'type': 'IfStatement', 'condition': condition, 'body': body}
        
        # elif
        elif token == 'elif':
            if last_token not in ['if','elif']: raise SyntaxError("Expected 'if' or 'elif' statement before 'elif' statement.")
            consume('elif')
            condition = ''
            while peek() not in [open_block_char, ':']: condition += consume()

            if '=' in condition and '==' not in condition: raise SyntaxError(f"Expected boolean operator, got '='. (did you mean to use '=='?)")
            
            condition = capitalize_if_true_false(condition)
            if peek() == open_block_char: body = parse_block() # if it sees an open block char (often '{' or '[') it'll parse the block
            
            elif peek() == ':': 
                consume(':')
                body = [parse_statement()]

            if peek() not in line_end_chars: raise SyntaxError(f"Expected line-ending character ({line_end_chars})...")
            consume()

            return {'type': 'ElifStatement', 'condition': condition, 'body': body}

        # else
        elif token == 'else':
            if last_token not in ['if','elif']: raise SyntaxError("Expected 'if' or 'elif' statement before 'else' statement.")
            consume('else')
            
            if peek() == open_block_char: body = parse_block() # if it sees an open block char (often '{' or '[') it'll parse the block
            
            elif peek() == ':': 
                consume(':')
                body = [parse_statement()]

            if peek() not in line_end_chars: raise SyntaxError(f"Expected line-ending character ({line_end_chars})...")
            consume()

            return {'type': 'ElseStatement', 'condition': condition, 'body': body}
        
        # repeat
        elif token == 'repeat':
            consume('repeat')
            condition = ''
            while peek() not in [open_block_char, ':']: condition += consume()

            if peek() == open_block_char: body = parse_block()

            elif peek == ':':
                consume(':')
                body = [parse_statement()]

            if peek() not in line_end_chars: raise SyntaxError(f"Expected line-ending character ({line_end_chars})...")
            consume()

            return {'type': 'RepeatStatement', 'condition': condition, 'body': body}
        
        # while
        elif token == 'while':
            consume('while')
            condition = ''
            while peek() not in [open_block_char, ':']: condition += consume()
            
            condition = capitalize_if_true_false(condition)
            if peek() == open_block_char: body = parse_block()

            elif peek == ':':
                consume(':')
                body = [parse_statement()]

            if peek() not in line_end_chars: raise SyntaxError(f"Expected line-ending character ({line_end_chars})...")
            consume()

            return {'type': 'WhileStatement', 'condition': condition, 'body': body}
        
        # for
        elif token == 'for':
            consume('for')
            #loop_variable = consume()
            if 'in' in peek():
                condition = peek()
                loop_variable = condition[:condition.index('in')]
                lexemes[pos] = condition[condition.index('in')+2:]

            else: raise SyntaxError(f"Expected 'in' after LoopVariable in ForStatement.")
            sequence = ''
            while peek() not in [open_block_char, ':']: sequence += consume() # REDO update to accept functions like 'range()' and stuff
            if peek() == open_block_char: body = parse_block()

            elif peek() == ':':
                consume(':')
                body = [parse_statement()]

            if peek() not in line_end_chars: raise SyntaxError(f"Expected line-ending character ({line_end_chars})...")
            consume()

            return {'type': 'ForStatement', 'loopVariable': loop_variable, 'sequence': sequence, 'body': body}

    # VARIABLES
        # integer
        elif token == 'int':
            consume('int')
            name = consume()
            if peek() != '=': raise SyntaxError("Expected '=' after Integer variable name.")
            consume('=')
            if peek() == '-' or peek() == '+': sign = consume()

            else: sign = ''
            
            if any(char not in ['1','2','3','4','5','6','7','8','9','0'] for char in peek()): raise ValueError("Float variable contains non-numerical characters.")
            value = sign + consume()
            value = int(value)
            if value == -0:
                value = 0

            if peek() not in line_end_chars: raise SyntaxError(f"Expected line-ending character ({line_end_chars})...")
            consume()
            defined_variables.append(name)
            return {'type': 'IntegerVariable', 'name': name, 'value': value}
            
        
        # boolean
        elif token == 'bool':
            consume('bool')
            name = consume()
            if peek() != '=': raise SyntaxError("Expected '=' after Bool variable name.")
            consume('=')
            value = consume()
            if value not in ['true','false']: raise ValueError("Boolean variable must be 'true' or 'false'.")
            value = capitalize_if_true_false(value)
            if peek() not in line_end_chars: raise SyntaxError(f"Expected line-ending character ({line_end_chars})...")
            consume()
            defined_variables.append(name)
            return {'type': 'BoolVariable', 'name': name, 'value': value}
        
        # float
        elif token == 'flt':
            consume('flt')
            name = consume()
            if peek() != '=': raise SyntaxError("Expected '=' after Float variable name.")
            consume('=')
            if peek() == '.': raise ValueError("Float variable decimal in wrong location.")
            if any(char not in ['1','2','3','4','5','6','7','8','9','0'] for char in peek()): raise ValueError("Float variable contains non-numerical characters.")
            value = consume()

            if peek() != '.': raise ValueError("Float variable missing decimal.")
            value += consume('.')

            if peek() == '.': raise ValueError("Float variable decimal in wrong location.")
            if any(char not in ['1','2','3','4','5','6','7','8','9','0'] for char in peek()): raise ValueError("Float variable contains non-numerical characters.")
            value += consume()

            value = float(value)

            if peek() not in line_end_chars: raise SyntaxError(f"Expected line-ending character ({line_end_chars})...")
            consume()
            defined_variables.append(name)
            return {'type': 'FloatVariable', 'name': name, 'value': value}
        # string
        elif token == 'str':
            consume('str')
            name = consume()
            if peek() != '=': raise SyntaxError("Expected '=' after String variable name.")
            consume('=')
            if peek() not in ["'", '"']: ValueError("String variable value must be inside of either double or single quotes.")
            if peek() == "'": 
                consume("'")
                current_quote_char = "'"

            elif peek() == '"':
                consume('"')
                current_quote_char = '"'

            value = f"{current_quote_char}{consume()}{current_quote_char}"
            consume(current_quote_char)

            if peek() not in line_end_chars: raise SyntaxError(f"Expected line-ending character ({line_end_chars})...")
            consume()
            defined_variables.append(name)
            return {'type': 'StringVariable', 'name': name, 'value': value}
        
        else:
            # Handle standard expressions
            if peek() == '\n': # dont include \n as expressions
                consume()
            else:
                
                expression = parse_expression()

                # variable assign statement
                if peek() == '=':
                    consume('=')
                    body = parse_expression()
                    attribute = None
                    if peek() == '.': attribute = parse_statement()
                    print("body: ", body)
                    return {'type': 'AssignmentStatement','name': parse_expression(), 'body': body, 'attribute': attribute}
                
                else: return parse_expression()
                    
                    
        
        if log: append_log("OK\n",False,False)

    # main parser loop
    ast = []
    while pos < len(lexemes):
        ast.append(parse_statement())
    return ast
