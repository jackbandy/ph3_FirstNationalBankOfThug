from PyCamellia import *
from Start import *
from State import *
from TestSuite import *
from types import *
import os
#from Singleton import *

#@Singleton
class Context:

    #if being tested
    def __init__(self, tester=None):
        self.current_state = Start(self)
        self.terminate = False
        self.saveString = ""
        if not(tester == None):
            print("Testing")
            self.debug = True
        else:
            self.debug = False
        self.loaded = False
        self.refine = 0
        self.nav = True
        self.file_name = "test1.txt"
        self.file = open(self.file_name, "r")
        self.tester = tester
    
    def main(self):
        print("Welcome to the PyCamellia incompressible flow solver!")
        while not self.terminate:
            self.current_state.main()

    def parse_error(self, user_input):
        print("Could not parse " + user_input)
        #if self.loaded or (self.debug and self.tester.handleError()):
        #    raise NameError("loaded response, " + str(user_input) + ", was unparsable")

    
    #Prints out data about the refinement
    def printRefine(self, energy, mesh):
        elements = mesh.numActiveElements()
        degrees = mesh.numGlobalDofs()
        refinementNumber = self.getRef()
        print("Mesh has %i elements and %i degrees of freedom." % (elements, degrees))
        print("Energy error after %i refinements: %0.3f" % (refinementNumber, energy))


    def switch_state(self, state):
        self.current_state = state

    #this method allows us to choose to either receive input from the user or a file
    def query(self, prompt):
        if self.loaded:
            line = self.file.readline()
            if line == "":#file empty
                raise NameError("incomplete file data")
            line = line.rstrip()#removes \n at the end
            answer = line
        else:#else take user input
            answer = self.take_user_input(prompt)
        self.saveString += answer + "\n"
        return answer

    #either asks the user for input or gets input from the test driver
    def take_user_input(self, prompt):
        if self.debug:
            answer = self.tester.response()
            if answer == "":#file empty
                self.debug = False
                print("file, " + self.tester.fileName + ",  empty")
                return raw_input(prompt)
            answer = answer.rstrip()#removes \n at the end
        else:
            answer = raw_input(prompt)
        return answer

    #verifies file exists
    def file_exists(self, prefix):
	name = prefix + ".txt"
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            if (name == f):#I think we want reading file names to be case sensitive
                return True
            False

    #opens file with given file name
    def upload_file(self, file_name):
        self.loaded = True
        self.file.close()
        self.file_name = file_name
        self.file = open(str(file_name) + ".txt", "r")
        refinement =  open(str(file_name) + "_refNum.txt", "r")
        line = refinement.readline().rstrip()
        self.refine = int(line)
        

    def getRef(self):
        return self.refine

    def incRef(self):
        self.refine += 1

    #Getter and Setter for 
    def setNav(self, boo):
        self.nav = boo

    def getNav(self):
        return self.nav

        
            

if __name__ =="__main__":
    c = Context()
    c.main()
