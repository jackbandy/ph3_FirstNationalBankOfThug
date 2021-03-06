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
	self.animateit = False
        self.refinementNumber = 0
        self.plotter = plotter.plotter()
        self.formCreator = FormCreator.FormCreator()
        self.interpreter2 = Interpreter2.Interpreter2()
    
    # String List Parameters
    #   String eq_type
    #   String pOrder
    #   String transOrSteady
    #   String Tuple dimensions
    #   String Tuple meshElements
    #   String reyNum (-1 if stokes)
    #   String Tuple List inflow (inflowPos, inflowXVel, inflowYVel)
    #   String List outflow
    #   
    def solve(self, eq_type, pOrder, state, dimensions, meshElements, reyNum, inflow, outflow):

        # set initial things once solve is called
        self.eq_type = eq_type
        self.refinementNumber = 0
        self.stringList = [eq_type, pOrder, state, dimensions, meshElements, reyNum, inflow, outflow]
        print(self.stringList)

        #Parse input data strings to the correct type
        eq_type_ = eq_type
        pOrder_ = int(pOrder)
        state_ = state
        dimensions_ = (float(dimensions[0]), float(dimensions[1]))
        meshElements_ = (int(meshElements[0]), int(meshElements[1]))
        reyNum_ = float(reyNum)
        inflowFunX_ = []
        inflowFunY_ = []
        inflowSpatialFilters_ = []
        for x in inflow:
            inflowSpatialFilters_.append(self.parsePos(x[0]))
            inflowFunX_.append(self.interpreter2.interpret(x[1]))
            inflowFunY_.append(self.interpreter2.interpret(x[2]))
        outflowSpatialFilters_ = []
        for x in outflow:
            outflowSpatialFilters_.append(self.parsePos(x))

        #Get a form from FormCreator (thank you woodson)
        if (reyNum_ == -1):
            self.form = self.formCreator.main(pOrder_, inflowSpatialFilters_, inflowFunX_, inflowFunY_, outflowSpatialFilters_, dimensions_, meshElements_, transient = (state == "Transient"))
        else:
            self.form = self.formCreator.main(pOrder_, inflowSpatialFilters_, inflowFunX_, inflowFunY_, outflowSpatialFilters_, dimensions_, meshElements_, re = reyNum_, transient = (state_ == "Transient"))


        #Solve
        self.solveForm()



    #subroutine for solving
    def solveForm(self):
        if self.stringList[0] == "Navier-Stokes":
            nonLinearThreshold = 1e-3
            maxSteps = 10
            normOfIncrement = 1
            stepNumber = 0
            while normOfIncrement > nonLinearThreshold and stepNumber < maxSteps:
                self.form.solveAndAccumulate()
                normOfIncrement = self.form.L2NormSolutionIncrement()
                stepNumber += 1
        
        else:
        #Stokes
          if(self.stringList[2] == "Transient"):
          #do fancy stuff
            self.animateit = True
          else:
            #this implies steady state stokes
            self.form.solve()




    def animateIt(self):
        dimensions_ = (float(self.stringList[3][0]), float(self.stringList[3][1]))
        meshElements_ = (int(self.stringList[4][0]), int(self.stringList[3][1]))

        dt = 0.1
        totalTime = 2.0
        numTimeSteps_ = int(totalTime / dt)

        order_ = int(self.stringList[1])

        self.plotter.plotAnim(self.form,order_,dimensions_,meshElements_,totalTime,dt)


            
    
    # Format and return the energy error to be printed
    def error(self):
        if self.stringList[0] == "Navier-Stokes":
            energy = self.form.solutionIncrement().energyErrorTotal()
        else:
            energy = self.form.solution().energyErrorTotal()
        mesh = self.form.solution().mesh()


        toRet =  "Initial mesh has %i elements and %i degrees of freedom.\n" % (mesh.numActiveElements(), mesh.numGlobalDofs())
        toRet = toRet + "Energy error after %i refinements: %0.3f" % (self.refinementNumber, energy)
        return toRet


    # Return a spatial filter given a string of limits
    def parsePos(self, input):
        altered = input.lower()
        altered = altered.translate(None, " ")#remove whitespace
        if altered.find(",") > -1: #if there are multiple spacial filters
            filters = altered.split(",")#split them
            filters_ = []
            for curr in filters:
                filters_.append(self.get_space_fil_helper(curr, input))
            
            toRet = SpatialFilter.intersectionFilter(filters_[0], filters_[1])
            i = 2
            while i < len(filters_):
                toRet = SpatialFilter.intersectionFilter(toRet, filters_[i])
                i = i + 1
            return toRet
        else:
            return self.get_space_fil_helper(altered, input)

    # ParsePos's helper method
    def get_space_fil_helper(self, assignment, prompt):
        is_x =  assignment.find("x") > -1
        if not is_x:
            if assignment.find("y") == -1:
                print "Could not parse " + assignment
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
            print "Could not parse " + assignment
            return self.parse()

    #takes a string like "0,1,2" and refines those elements
    def manualHRefine(self, elements_string):
        self.refinementNumber += 1
        cells = self.parse_cells(elements_string)
        self.form.solution().mesh().hRefine(cells)
        
    #takes a string like "0,1,2" and refines those elements
    def manualPRefine(self, elements_string):
        self.refinementNumber += 1
        cells = self.parse_cells(elements_string)
        self.form.solution().mesh().pRefine(cells)
    
    def autoHRefine(self):
        self.refinementNumber += 1
        self.form.hRefine()
        self.solveForm()

    def autoPRefine(self):
        self.refinementNumber += 1
        self.form.pRefine()
        self.solveForm()

    # Takes a string and returns a list of int
    # This is for turning the manual refine functions
    def parse_cells(self, data):
        cells_refine = []
        for val in data:
                try:
                    cells_refine.append(int(val))
                except ValueError:
                    raise ValueError("Could not convert to an int")
        return cells_refine


    # Save everything
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

    #Load Everything
    def load(self, fileName):
        #loading stringlist and refinement #
        file = open(fileName, 'rb')
        self.stringList = pickle.load(file)
        self.refinementNumber = pickle.load(file)
        file.close()
        #if Stokes
        if self.stringList[0] == "Stokes":
            self.form = StokesVGPFormulation(2, False)
            self.form.initializeSolution(fileName, int(self.stringList[1]))
        #if NS
        elif self.stringList[0] == "Navier-Stokes":
            self.form = NavierStokesVGPFormulation(fileName, 2, float(self.stringList[5]), int(self.stringList[1]))
        return self.stringList





    # Tell plotter.py what to plot (otherwise plot a puppy)
    def plot(self, pltstr):
        if (self.form == None):
            return "puppies3.jpg"
	if (self.animateit == True):
	    self.animateIt()
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

        return "puppies3.jpg"
