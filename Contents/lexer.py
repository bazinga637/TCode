def lexer(source_code):
            
    SYMBOLS = ['/','\\',
               ':',';',
               '+','-','=','#','*',
               '(',')','[',']','{','}',
               '.',',',"'",'"','\n',
    ]

    KEYWORDS = [
        'if','elif','else','repeat','while','for', # conditionals
        'and','or','true','false', # booleans
        'int','bool','str','flt', # variables
        'func', # defining
    ]

    ## leave values blank
    lexemes = []
    current_lexeme = ''
    ##

    ignored_chars = [' ','\t'] # whitespaces that dont matter in the compiler
    ignore_chars = True
    current_quote = ''
    for i, char in enumerate(source_code):
        
        # doesn't ignore any characters inside strings (both types of quotes)
        if char == "'" and current_quote != '"':
            current_quote = "'"
            ignore_chars = not ignore_chars

        elif char == '"' and current_quote != "'":
            current_quote = '"'
            ignore_chars = not ignore_chars


        if char not in ignored_chars or ignore_chars == False:
            current_lexeme += char

        if (i + 1 < len(source_code)):
            next_char = source_code[i + 1]

            if next_char in SYMBOLS or char in SYMBOLS or current_lexeme in KEYWORDS:
                if current_lexeme != '':
                    lexemes.append(current_lexeme)
                    current_lexeme = ''

    if current_lexeme:
        lexemes.append(current_lexeme)

    return lexemes
