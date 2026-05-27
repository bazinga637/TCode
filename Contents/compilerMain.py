# open script file
with open('script.tc', 'r') as file_input:
    file_read = file_input.read()
    if file_read != '':
        user_input = file_read

from lexer import lexer
from parser import parser
from generator import generate_python
#from generator import generate_c

from datetime import datetime

# get starting stuff logged
def append_log(input, logdate=False, logtime=True):
    if logtime:
        with open('.log', 'a') as log: log.write(f"\n{str(datetime.now().time())}:  ")

    with open('.log', 'a') as log: log.write(input)
    
    if logdate: 
        with open('.log', 'a') as log: log.write(str(datetime.now().date()))

def append_error(error):
    append_log("\n",False,False)
    append_log(f"ERROR: {error}\n")

# Start running code

start_time = datetime.now()
append_log(f"New session: ", True)
append_log("Compiler Start\n")

try: # lex
    append_log("Lexing...")
    lexemes = lexer(user_input)
    append_log(f"Lexemes: {lexemes}\n\n")

except Exception as error:
    append_error(error)
else:

    try: # parse
        append_log("Parsing...\n")
        ast = parser(lexemes)
        append_log(f"AST: {ast}\n")

    except Exception as error:
        append_error(error)
    else:

        try: # generate
            append_log("Generating code...")
            #code = generate_c(ast) # this dont work
            code = generate_python(ast)
            code_type = 'Python'
            append_log(f"{code_type} code:\n\n{code}\n")

        except Exception as error:
            append_error(error)
        else:

            try: # execute
                append_log("Executing...")
                exec(code)
                append_log("Executed successfully.\n")

            except Exception as error:
                append_error(error)

append_log(f"Run time: {datetime.now() - start_time}")
append_log("End session ", True)
append_log('\n---------------------------------------------\n', False, False)