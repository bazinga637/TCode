
import platform
import os

from datetime import datetime,time # because extensions dont work when executing another script from here (datetime used in compiler main)

current_os = platform.system()

if current_os == "Windows":
    import msvcrt
elif current_os == "Linux":
    import curses

def clear_terminal():
    # 'nt' is the name for Windows; 'posix' includes Linux, macOS, etc.
    os.system('cls' if os.name == 'nt' else 'clear')


def print_and_get_char_Windows(lines, current_line, line_position):
    clear_terminal()
    for x in range(len(lines)): 
        line_to_print = lines[x]
        if x == current_line:
            line_to_print = line_to_print[:line_position] + '|' + line_to_print[line_position:]
        print(f"\033[90m{x + 1} . {' ' * (4 - len(str(x + 1)))}\033[0m", line_to_print) # change color to gray, print line number, reset color, print line
    return msvcrt.getch()

def print_and_get_char_Linux(stdscr,lines, current_line, line_position):
    stdscr.clear()
    curses.nonl()
    for x in range(len(lines)): 
        line_to_print = lines[x]
        if x == current_line:
            line_to_print = line_to_print[:line_position] + '|' + line_to_print[line_position:]
        stdscr.addstr(x,0,f"{x + 1} . {line_to_print}")
    stdscr.refresh()
    stdscr.keypad(True)

    key_map = {
        curses.KEY_UP:          b'H',
        curses.KEY_DOWN:        b'P',
        curses.KEY_LEFT:        b'K',
        curses.KEY_RIGHT:       b'M',
        curses.KEY_DC:          b'S', # Delete key
        curses.KEY_ENTER:       b'\r',
        curses.KEY_BACKSPACE:   b'\x08',
        127:                    b'\x08',
    }
    key = stdscr.getch()
    # Check if it's a \xe0 key
    if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_DC]:
        return b'\xe0' + key_map[key]
    
    # Check for other special keys
    if key in key_map:
        return key_map[key]
    return key.to_bytes(1, 'big') 


def add_to_line(lines, current_line, line_position, input):
    lines[current_line] = lines[current_line][:line_position] + input + lines[current_line][line_position:]
    line_position += 1
    return lines[current_line], line_position


def main(current_os):
    clear_terminal()

    allowed_commands = 'wqe'

    current_line = 0 # what line is currently being edited
    line_position = 1 # what character in current_line is being edited

    with open('script.tc', 'r') as script:
        lines = script.read().splitlines() # list of all lines

    print('')
    while True:
        print("\033[?25l", end="") # makes terminal cursor invisible


        if current_os == "Windows":
            char = print_and_get_char_Windows(lines, current_line, line_position)
        elif current_os == "Linux":
            char = curses.wrapper(print_and_get_char_Linux,lines, current_line, line_position)


        # COMMAND KEY - Key to be able to write commands
        if char == b'\x1b': # escape
            command = input('\n:').lower()
            print(command)
            if set(command).issubset(allowed_commands):
                clear_terminal()

                if 'w' in command: # writes text to script file using 'w' for write
                    with open('script.tc', 'w') as script:
                        for y in lines:
                            script.write(f"{y}\n")
                            
                if 'e' in command: # executes file with compiler using 'e' for exec
                    with open("Contents/compilerMain.py",'r') as compiler:
                        exec(compiler.read())
                        input('Press enter to continue...')
                
                if 'q' in command: # q is for quit
                    if 'w' not in command:
                        if input("Your progress will not save. Enter 'q' to quit anyways...").lower() == 'q': break

                    else: break

                        
        # TAB
        elif char == b'\t':
            lines[current_line], line_position = add_to_line(lines, current_line, line_position, '    ')
            line_position += 3
        
        # BACKSPACE
        elif char == b'\x08':
            if line_position == 0 and current_line != 0: # removes current line if pressing backspace at the start of the line, but not the first line
                line_position = len(lines[current_line-1])
                lines[current_line-1] += lines[current_line]
                del lines[current_line] # remove line
                current_line -= 1
                
            elif line_position != 0:
                lines[current_line] = lines[current_line][:line_position-1] + lines[current_line][line_position:] # backspace
                line_position -= 1 # move backwards to compensate for backspace thing
 
        
        # RETURN/ENTER
        elif char == b'\r':
            after_line_position = lines[current_line][line_position:]
            if after_line_position != '':
                lines[current_line] = lines[current_line][:-len(after_line_position)] # remove lines after line_position
            lines.insert(current_line + 1, after_line_position) # add new line, adds characters after line_position
            current_line += 1 # move to new line
            line_position = 0

        # WEIRD KEYS THAT NEED ANOTHER GETCH
        elif b'\xe0' in char:
            if current_os == "Windows": subkey = msvcrt.getch()
            elif current_os == "Linux": subkey = char.replace(b'\xe0',b'',1)             
            # DELETE
            if subkey == b'S':
                lines[current_line] = lines[current_line][:line_position] + lines[current_line][line_position+1:]

            # ARROW KEYS
            elif subkey == b'H' and current_line > 0: # up arrow
                current_line -= 1
                if line_position > len(lines[current_line]):
                    line_position = len(lines[current_line])

            elif subkey == b'P' and current_line < len(lines) - 1: # down arrow
                current_line += 1
                if line_position > len(lines[current_line]):
                    line_position = len(lines[current_line])

            elif subkey == b'K' and line_position != 0: # left arrow
                line_position -=  1

            elif subkey == b'M' and line_position != len(lines[current_line]): # right arrow
                line_position += 1
                
        
        # EVERYTHING ELSE
        else:
            lines[current_line], line_position = add_to_line(lines, current_line, line_position, str(char.decode('ascii')))
        
    clear_terminal()
        

main(current_os)
