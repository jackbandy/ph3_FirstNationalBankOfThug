from PyCamellia import *
import Interpreter2
import pickle
import random
import plotter
import FormCreator
import re

class Controller(object):

    def __init__(self):
        self.stringList = []
        self.form = None
        self.refinementNumber = 0
        self.plotter = plotter.plotter()
        self.formCreator = FormCreator.FormCreator()
        self.interpreter2 = Interpreter2.Interpreter2()
        self.puppies = ['puppies.jpg','puppies2.jpg','puppies3.jpg','puppies4.jpg','puppies5.jpg','puppies6.jpg','puppies7.jpg','puppies8.jpg','puppies9.jpg','puppies10.jpg']
    #String List
    #   String eq_type
    #   String pOrder
    #   String transOrSteady
    #   String Tuple dimensions
    #   String Tuple meshElements
    #   String reyNum (-1 if stokes)
    #   String Tuple List inflow
    #   String List outflow
    #   
    def solve(self, eq_type, pOrder, state, dimensions, meshElements, reyNum, inflow, outflow):
        #for solveForm
        self.eq_type = eq_type

        self.stringList = [eq_type, pOrder, state, dimensions, meshElements, reyNum, inflow, outflow]
        
        #Parse input data strings to the correct type
        eq_type_ = eq_type
        pOrder_ = int(pOrder)
        state_ = state
        dimensions_ = (float(dimensions[0]), float(dimensions[1]))
        meshElements_ = (int(meshElements[0]), int(meshElements[1]))
        reyNum_ = int(reyNum)
        inflowFunX_ = []
        inflowFunY_ = []
        inflowSpatialFilters_ = []
        for x in inflow:
            inflowSpatialFilters_.append(self.parsePos(x[0]))
            inflowFunX_.append(self.interpreter2.interpret(x[1]))
            inflowFunY_.append(self.interpreter2.interpret(x[2]))
        outflowSpatialFilters_ = []
        for x in outflow:
            outflowSpatialFilters_.append(self.ParsePos(x))

        #Get a form from FormCreator - Woodson?
        if (reyNum_ == -1):
            self.form = self.formCreator.main(pOrder_, inflowSpatialFilters_, inflowFunX_, inflowFunY_, outflowSpatialFilters_, dimensions_, meshElements_, transient = (state == "transient"))
        else:
            self.form = self.formCreator.main(pOrder_, inflowSpatialFilters_, inflowFunX_, inflowFunY_, outflowSpatialFilters_, dimensions_, meshElements_, re = reyNum_, transient = (state_ == "transient"))


        #Solve
        self.solveForm()



    #subroutine for resolving when refining
    def solveForm(self):
        if self.eq_type == "Navier-Stokes":
            nonLinearThreshold = 1e-3
            maxSteps = 10
            normOfIncrement = 1
            stepNumber = 0
            while normOfIncrement > nonLinearThreshold and stepNumber < maxSteps:
                self.form.solveAndAccumulate()
                normOfIncrement = self.form.L2NormSolutionIncrement()
                stepNumber += 1
            mesh = self.form.solution().mesh()
            energy = self.form.solutionIncrement().energyErrorTotal()
        
        else:
            self.form.solve()
            mesh = self.form.solution().mesh()
            energy = self.form.solution().energyErrorTotal()

            
    
    def error(self):
        if self.stringList[0] == "Navier-Stokes":
            energy = self.form.solutionIncrement().energyErrorTotal()
        else:
            energy = self.form.solution().energyErrorTotal()
        mesh = self.form.solution().mesh()

        print type(self.form)

        toRet =  "Initial mesh has %i elements and %i degrees of freedom.\n" % (mesh.numActiveElements(), mesh.numGlobalDofs())
        toRet = toRet + "Energy error after %i refinements: %0.3f" % (self.refinementNumber, energy)
        return toRet


    """
    #Returns a spatial filter given a string that is 
    def parsePos(self, input):
        inputData = re.split('=|<|>|,', input)
        input = re.split('( )*([0-9]*\.[0-9]+|[0-9]+)( )*', input)
        spatial1 = SpatialFilter.matchingX(float(0))
        spatial2 = SpatialFilter.greaterThanY(float(0))

        if input[0] == 'x=':
            spatial1 = SpatialFilter.matchingX(float(inputData[1]))
            if input[4] == ',y>':
                spatial2 = SpatialFilter.greaterThanY(float(inputData[3]))
            elif input[4]== ',y<':
                spatial2 = SpatialFilter.lessThanY(float(inputData[3]))
        elif input[0] == 'x>':
            spatial1 = SpatialFilter.greaterThanX(float(inputData[1]))
            #must be y=	
            spatial2 = SpatialFilter.matchingY(float(inputData[3]))
        elif input[0] == 'x<':
            spatial1 = SpatialFilter.lessThanX(float(inputData[1]))	
            spatial2 = SpatialFilter.matchingY(float(inputData[3]))
        elif input[0] == 'y=':
            spatial1 = SpatialFilter.matchingY(float(inputData[1]))
            if input[4]==',x>':
                spatial2 = SpatialFilter.greaterThanX(float(inputData[3]))
            elif input[4]==',x<':
                spatial2 = SpatialFilter.lessThanX(float(inputData[3]))
        elif input[0] == 'y>':
            spatial1 = SpatialFilter.greaterThanY(float(inputData[1]))
            spatial2 = SpatialFilter.matchingX(float(inputData[3]))
        elif input[0] == 'y<':
            spatial1 = SpatialFilter.lessThanY(float(inputData[1]))
            spatial2 = SpatialFilter.matchingX(float(inputData[3]))
        return spatial1 and spatial2
        """

     #takes a string and returns a spacial filter
    def ParsePos(self, input):
        answer = self.context.query(input)
        altered = answer.lower()
        altered = altered.translate(None, whitespace)#remove whitespace
        if altered.find(",") > -1: #if there are multiple spacial filters
            halves = altered.split(",")#split them
            filter1 = self.get_space_fil_helper(halves[0],input)
            filter2 = self.get_space_fil_helper(halves[1],input)
            return SpatialFilter.intersectionFilter(filter1, filter2)
        else:
            return self.get_space_fil_helper(altered, input)

    #ParsePos's helper method
    def get_space_fil_helper(self, assignment, prompt):
        is_x =  assignment.find("x") > -1
        if not is_x:
            if assignment.find("y") == -1:
                self.context.parse_error(assignment)
                return self.get_space_fil(prompt)
        #error here
        if assignment.find("=") > -1:
            if is_x:
                return SpatialFilter.matchingX(float(assignment.translate(None, "x=")))
            else:
                return SpatialFilter.matchingY(float(assignment.translate(None, "y=")))
        elif assignment.find(">") > -1:
            if is_x:
                return SpatialFilter.greaterThanX(float(assignment.translate(None, "x>")))
            else:
                return SpatialFilter.greaterThanY(float(assignment.translate(None, "y>")))
        elif assignment.find("<") > -1:
            if is_x:
                return SpatialFilter.lessThanX(float(assignment.translate(None, "x<")))
            else:
                return SpatialFilter.lessThanY(float(assignment.translate(None, "y<")))
        else:
            self.context.parse_error(assignment)
            return self.parse()

    #takes a string like "0,1,2" and refines those elements
    def manualHRefine(self, elements_string):
        cells = self.parse_cells(elements_string)
        self.form.solution().mesh().hRefine(cells)
        
    #takes a string like "0,1,2" and refines those elements
    def manualPRefine(self, elements_string):
        cells = self.parse_cells(elements_string)
        self.form.solution().mesh().pRefine(cells)
    
    def autoHRefine(self):
        self.form.hRefine()
        self.solveForm()

    def autoPRefine(self):
        self.form.pRefine()
        self.solveForm()

        #takes a string and returns a list of int
        #this is for turning the manual refine functions
    def parse_cells(self, data):
        cells_refine = []
        new_stuff = (num.split(','))
        for val in new_stuff:
                try:
                    cells_refine.append(int(val))
                except ValueError:
                    raise ValueError("Could not convert to an int")
        return cells_refine


        
    def save(self, fileName):
        if (self.form != None):
            #saving stringlist and refinement #
            file = open(fileName, 'wb')
            pickle.dump(self.stringList, file)
            pickle.dump(self.refinementNumber, file)
            file.close()
            #saving form
            self.form.save(fileName)
        else:
            raise Exception

    def load(self, fileName):
        try:
            print("Line1")
            #loading stringlist and refinement #
            file = open(fileName, 'rb')
            self.stringList = pickle.load(file)
            #if stokes use: initializeSolution(std::string savePrefix, int fieldPolyOrder, int delta_k = 1, FunctionPtr forcingFunction = Teuchos::null);
            self.refinementNumber = pickle.load(file)
            file.close()
            print "File Found"
            #if Stokes
            if self.stringList[0] == "Stokes":
                self.form = StokesVGPFormulation(2, False)
                self.form.initializeSolution(fileName, self.stringList[1])
            #if NS
            elif self.stringList[0] == "Navier-Stokes":
                self.form = NavierStokesVGPFormulation(fileName, 2, self.stringList[5], self.stringList[1])
        except Exception as inst:
            print type(inst)
            raise Exception




    def plot(self, pltstr):
        if (self.form == None):
            return random.choice(self.puppies)
        if (pltstr == "u1"):
            return self.plotter.plotU1(self.form)
        elif (pltstr == "u2"):
            return self.plotter.plotU2(self.form)
        elif (pltstr == "p"):
            return self.plotter.plotP(self.form)
        elif (pltstr == "stream"):
            return self.plotter.plotStream(self.form)
        elif (pltstr == "mesh"):
            return self.plotter.plotMesh(self.form)
        elif (pltstr == "error"):
            return self.plotter.plotError(self.form, self.stringList[0] == "Stokes")

        return random.choice(self.puppies)
        
         

    
