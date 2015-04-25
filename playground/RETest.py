import re
from string import *

print "Input a Regular Expression"
re = re.compile(raw_input(">> "))
while True:
    print "Enter a test input (quit to exit the program)"
    input = raw_input(">> ")
    input = input.replace(" ", "")
    if (input == ("quit")):
        break
    m = re.findall(input)
    if (m != []):
        print (m) 
    else:
        print False

