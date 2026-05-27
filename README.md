# TCode

FINALLY got this crap working

This is still super early in development, I just got it working on 05/22/26 at 10:14 pm

My first actually kinda big project, so it won't stand up to any professional standards it just works for the most part

General purpose language written in python as a fun challange in grade 10 and (so far) has no real use.

Its called TCode cuz its code made by the T man

TCode file format is .tc, it wasnt used all that much and makes sense

almost everything here requires a python compiler to run. might do something about it later.

push and pull powershell scripts are just for me to be able to easily push and pull to git repo

script.tc is the file that the compiler will run, not sure how else I'm gonna deal with that part I havent thought about it

Error catcher and stuff is kinda bad and underdeveloped, not sure if it was a good idea to do all that in my parser or not but whatever (it WILL be updated dont worry (hopefully))

## Supported Things to do

there's if, elif, else, for, repeat (basically a for range() loop), while

built in functions like print(), get() for dictionaries, input() which works as it does in python

## Syntax

mostly like python but theres a few differences.
EVERYTHING is subject to change as I don't know what I want this to be like yet

### Comments

comments are with double slashes // and whatever this is /*    */

### Variables

booleans are lowercase (true, false)

variables need to be initialized with variable type (int, flt, bool, str) before being used

Right now variables can only be initialized with directly whatever type the var type is (int can only initialize to integer characters, that kinda stuff)

### Lines and stuff idk

nesting is possible in conditional statements (if, else, etc...) with curly brackets {}

lines are ended by semicolon ; or new lines \n, just like python

## Text Editor

inside /Contents the text editor.py is a terminal text editor I made that works with Windows and Linux. The editor uses the script.tc file.

To make commands press Escape and type commands there.

List of commands are 'q' for quit which asks for confirmation if not paired with 'w' which is write (or save). 'e' executes the script through the compiler.
