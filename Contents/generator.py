
def generate_python(ast, indent_level=0):
    python_code = ""
    indent = "    " * indent_level

    ast = [item for item in ast if item is not None] # removes None
    #print('AST: ',ast, type(ast))
    for node in ast:
        
        if node is None: continue
        #print('node:  ', node, ' var type:  ',type(node))
        node_type = node.get('type')

        # Handle Variables: (str, bool, int, flt)
        if node_type in ['IntegerVariable', 'FloatVariable', 'BoolVariable','StringVariable']:
            python_code += f"{indent}{node['name']} = {node['value']}\n" # add variable statement

        elif node_type == 'VariableExpression':
            if node['attribute'] == None or 'attribute' not in node:
                python_code += f"{node['expression']}\n"
            else:
                python_code += f"{node['expression']}.{generate_python([node['attribute']])}\n"

        elif node_type == 'MathExpression':
            python_code += f"{node['operand']}{node['operator']}{node['quotient']}\n"
        
        # Handle List Variables: {tables}, [lists]
        elif node_type == 'ListExpression':
            python_code += f"[{node['body']}]"

        elif node_type == 'TableExpression':
            python_code +=f"{'{'}{''.join(node['body'])}{'}'}\n"

        #Handle Functions: def name(args):
        elif node_type == 'FunctionDefineStatement':
            arguements = ", ".join(node['arguements'])
            python_code += f"{indent}def {node['name']}({arguements}):\n"# add function statement
            # Recursively generate body with extra indentation
            python_code += generate_python(node['body'], indent_level + 1) # statement body
        
        elif node_type == 'FunctionCall':
            arguements = ", ".join(node['arguements'])
            python_code += f"{indent}{node['name']}({arguements})\n"# add function statement

        elif node_type == 'ReturnStatement':
            python_code += f"{indent}return {generate_python([node['arguement']])}"

        elif node_type == 'AssignmentStatement':
            python_code += f"{indent}{node['name']} = {generate_python([node['body']])}"
            #if node['attribute']: python_code += f".{node['attribute']}\n" # only add attribute if there is one


        # Handle Conditional Statements
        # if
        elif node_type == 'IfStatement':
            keyword = "if"
            python_code += f"{indent}{keyword} {node['condition']}:\n" # add if statement
            python_code += generate_python(node['body'], indent_level + 1) # statement body
        #elif
        elif node_type == 'ElifStatement':
            keyword = "elif"
            python_code += f"{indent}{keyword} {node['condition']}:\n"
            python_code += generate_python(node['body'], indent_level + 1)
        # else
        elif node_type == 'ElseStatement':
            keyword = "else"
            python_code += f"{indent}{keyword}:\n"
            python_code += generate_python(node['body'], indent_level + 1)
        # repeat
        elif node_type == 'RepeatStatement':
            keyword = "for"
            python_code += f"{indent}{keyword} _ in range({node['condition']}):\n"
            python_code += generate_python(node['body'], indent_level + 1)
        # while
        elif node_type == 'WhileStatement':
            keyword = "while"
            python_code += f"{indent}{keyword} {node['condition']}:\n"
            python_code += generate_python(node['body'], indent_level + 1)
        # for
        elif node_type == 'ForStatement':
            keyword = "for"
            python_code += f"{indent}{keyword} {node['loopVariable']} in {node['sequence']}:\n"
            python_code += generate_python(node['body'], indent_level + 1)
        
    
    return python_code


# ts does NOT work
def generate_c(ast, indent_level=0):
    c_code = ""
    indent = "    " * indent_level

    ast_variable_type_list = ['IntegerVariable', 'FloatVariable', 'BoolVariable','StringVariable']
    c_variable_type_list = ['int', 'float', 'bool','char']

    for node in ast:
        
        if node is None: continue # some nodes are None so this just skips over to prevent errors

        node_type = node.get('type')

        # Handle Print: print(a, b)
        if node_type == 'PrintFunction':
            arguements = ", ".join(node['arguements'])
            c_code += f"{indent}printf({arguements}); " # add variable statement

        # Handle Variables: (str, bool, int, flt)
        elif node_type in ast_variable_type_list:
            value = node['value']
            var_type = c_variable_type_list[ast_variable_type_list.index(node_type)] # finds variable type by comparing position in ast_variable_type_list to position in c_variable_type_list
            if var_type == 'bool': value = value.lower() # turns True into true
            if var_type == 'char': char_list = '[]' 
            else: char_list = ''
            c_code += f"{indent}{var_type} {node['name']}{char_list} = {value}; " # add variable statement

        #Handle Functions: def name(args):
        elif node_type == 'Function':
            arguements = ", ".join(node['arguements'])
            c_code += f"{indent}void {node['name']}({arguements}) {'{'}" # add function statement, {'{'} is just to add {
            # Recursively generate body with extra indentation
            c_code += generate_c(node['body'], indent_level + 1) # statement body
            c_code += '}'


        # Handle If/Elif Statements
        elif node_type == 'IfStatement':
            keyword = "if"
            c_code += f"{indent}{keyword} ({node['condition']}) {'{'}"# add if statement
            c_code += generate_c(node['body'], indent_level + 1) # statement body
            c_code += '}'

        elif node_type == 'ElifStatement':
            keyword = "elif"
            c_code += f"{indent}{keyword} ({node['condition']}) {'{'}"
            c_code += generate_c(node['body'], indent_level + 1)
            c_code += '}'
        
        elif node_type == 'ElseStatement':
            keyword = "else"
            c_code += f"{indent}{keyword} {'{'}"
            c_code += generate_c(node['body'], indent_level + 1) #
            c_code += '}'

    #c_code = f"int main(): {'{'}\n{c_code}\nreturn 0;\n{'}'}" # adds main func stuff fix for funcs and stuff
    return c_code
