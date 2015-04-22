from PyCamellia import *
import re
from string import *
import math

class Interpreter2():
    def interpret(self, string):
        self.string = string
        self.string.replace(" ", "")#removes spaces
        try:
            return self.iterateString(self.string)
        except NameError:
            raise NameError

    #exponents are only constant integers
    def retExp(self, base, expo):
        if (expo == -1):
            return 1/base
        if (expo < -2):
            return (1/base)/self.retExp(base, expo + 1)
        if (expo == 0):
            return 1
        if (expo == 1):
            return base
        if (expo > 1):
            return base * self.retExp(base, expo - 1)

    def iterateString(self, string):
        position = 0
        stack = []
        neg_bool = False
        while position < len(string):
            if (self.isNumPart(string[position])):
                if (neg_bool):
                    numString = "-"
                    neg_bool = False
                else:
                    numString = ""
                while position < len(string):
                    if self.isNumPart(string[position]):
                        numString += string[position]
                        position += 1
                    else:
                        break
                try:
                    convert = float(numString)
                    new_function = Function.constant(convert)
                    stack.append(new_function)
                except ValueError:
                    raise NameError("Invalid Syntax")

            elif(string[position] == "("):
                start_pos = position
                l_paren = 1
                while (l_paren > 0):
                    position += 1
                    if (position >= len(string)):
                        raise NameError("No end Parenthesis")
                    elif (string[position] == '('):
                        l_paren += 1
                    elif (string[position] == ')'):
                        l_paren -= 1
                if not(start_pos + 1 == position):
                    try:
                        new_fun = self.iterateString(string[start_pos + 1:position])
                        stack.append(new_fun)
                    except NameError, e:
                        raise e
                position += 1

            elif(string[position] == ")"):
                raise NameError("Invalid Syntax")
                
            elif (string[position] == ("x")):
                if (neg_bool):
                    new_fun = Function.constant(-1)*Function.xn(1)
                    stack.append(new_fun)
                    neg_bool = False
                else:
                    new_fun = Function.xn(1)
                    stack.append(new_fun)
                position += 1

            elif (string[position] == ("y")):
                if (neg_bool):
                    new_fun = Function.constant(-1)*Function.yn(1)
                    stack.append(new_fun)
                    neg_bool = False
                else:
                    new_fun = Function.yn(1)
                    stack.append(new_fun) 
                position += 1

            elif (string[position] in ("+", "-")):
                if (stack[-1:] in (['*'],['+'],['-'],['/'],['^'],[])):
                    if(string[position]== "-"):
                        neg_bool = True
                else:
                    stack.append(string[position])
                position += 1

            elif (string[position] in ("*", "/","^","e")):
                stack.append(string[position])
                position += 1
            
            else:
                position += 1
                

        #done with looping and tokenizing
        #variables & constatnts are Function Pointers
        #operators are strings
        #OofO
        position = 0
        while (position < len(stack)):
            if(stack[position] == '^'):
                new_stack = stack[:position -1]
                doub = math.floor(Function.evaluate(stack[position + 1],1.0,1.0))
                new_fun = self.retExp(stack[position - 1],doub)
                new_stack.append(new_fun)
                new_stack.extend(stack[position+2:])
                stack = new_stack
            else:
                position += 1

        position = 0
        while (position < len(stack)):
            if(stack[position] == 'e'):
                new_stack = stack[:position -1]
                doub =math.floor(Function.evaluate(stack[position + 1],1.0,1.0))
                new_fun = stack[position -1] * self.retExp(10,doub)
                new_stack.append(new_fun)
                new_stack.extend(stack[position+2:])
                stack = new_stack
            else:
                position += 1

        position = 0
        while (position < len(stack)):
            if(stack[position] == ('*')):
                new_stack = stack[:position -1]
                new_fun = (stack[position - 1]*stack[position + 1])
                new_stack.append(new_fun)
                new_stack.extend(stack[position+2:])
                stack = new_stack
            else:
                position += 1

        position = 0
        while (position < len(stack)):
            if(stack[position] == '/'):
                new_stack = stack[:position -1]
                new_fun = (stack[position - 1]/stack[position + 1])
                new_stack.append(new_fun)
                new_stack.extend(stack[position+2:])
                stack = new_stack
            else:
                position += 1
        #Two Function ptrs in a row
        position = 0
        while (position < len(stack) -1):
            if (type(stack[position]) is  FunctionPtr):
                if (type(stack[position + 1]) is  FunctionPtr):
                    new_stack = stack[:position]
                    new_fun = stack[position]*stack[position + 1]
                    new_stack.append(new_fun)
                    new_stack.extend(stack[position+2:])
                    stack = new_stack
                else:
                    position += 1
            else:
                position += 1
        position = 0
        while (position < len(stack)):
            if(stack[position] == ('+')):
                new_stack = stack[:position -1]
                new_fun = stack[position - 1] + stack[position + 1]
                new_stack.append(new_fun)
                new_stack.extend(stack[position+2:])
                stack = new_stack
            else:
                position += 1
        position = 0
        while (position < len(stack)):
            if(stack[position] == ('-')):
                new_stack = stack[:position -1]
                new_fun = (stack[position - 1]-stack[position + 1])
                new_stack.append(new_fun)
                new_stack.extend(stack[position+2:])
                stack = new_stack
            else:
                position += 1
                
        #operate
        if(len(stack)<1):
            raise NameError
        else:
            return stack[0]


    def isNumPart(self, string):
        if string in ('.','0','1','2','3','4','5','6','7','8','9'):
            return True
        return False


