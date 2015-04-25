from PyCamellia import *
import Interpreter2
import pickle
import random
#import plotter

class Controller(object):

    def __init__(self):
        self.stringList = []
        self.form = None
        self.refinementNumber = 0
        #self.plotter = plotter.plotter()
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

        self.stringList = [eq_type, pOrder, state, dimensions, meshElements, reyNum, inflow, outflow]
        
        #Parse input data strings to the correct type
        eq_type_ = eq_type
        pOrder_ = int(eq_type)
        state_ = state
        dimensions_ = (float(dimensons[0]), float(dimensions[1]))
        meshElements_ = (int(meshElements[0]), int(meshElements[1]))
        reyNum_ = int(reyNum)
        inflowPos_ = []
        inflowSpatialFilters_ = []
        for x in inflowFunctions:
            inflowSpatialFilters_.append(parsePos(x[0]))
            inflowFunctions_.append(self.interpreter2.interpret(x[1]))
        outflowSpatialFilters_ = []
        for x in outflow:
            outflowSpatialFilters_.append(parsePos(x))


        #Get a form with FormCreator - Woodson?
        

        #Solve
        if eq_type == "Navier-Stokes":
            nonLinearThreshold = 1e-3
            maxSteps = 10
            normOfIncrement = 1
            stepNumber = 0
            while normOfIncrement > nonLinearThrehshold and stepNumber < maxSteps:
                self.form.solveAndAccumulate()
                normOfIncrement = self.form.L2NormSolutionIncrement()
                stepNumber += 1
            mesh = self.form.solution.mesh()
            energy = self.form.solutionIncrement().energyErrorTotal()
        
        else:
            self.form.solve()
            mesh = self.form.solution().mesh()
            energy = self.form.solution().energyErrorTotal()

            
    
    def error():
        if self.stringList[0] == "Navier-Stokes":
            energy = self.form.solutionIncrement().energyErrorTotal()
        else:
            energy = self.form.solution().energyErrorTotal()
        mesh = self.form.solution.mesh()

        toRet =  "Initial mesh has %i elements and %i degrees of freedom." % (mesh.numActiveElements(), mesh.numGlobalDofs())
        toRet = toRet + "Energy error after %i refinements: %0.3f" % (self.refinementNumber, energy)
        return toRet



    #Returns a spatial filter given a string that is 
    def parsePos(input):
        inputData = re.split('=|<|>|,', input)
        input = re.split('( )*([0-9]*\.[0-9]+|[0-9]+)( )*', input)
		
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

    def plot(self, pltstr):
        return random.choice(self.puppies)
        
    def save(self, fileName):
        #saving stringlist
        file = open(fileName, 'wb')
        pickle.dump(self.stringList, file)
        file.close
        #saving form solution
        self.form.solution().save(fileName)

    def load(self, fileName):
        #loading stringlist
        file = open(fileName, 'rb')
        self.stringList = pickle.load(file)
        file.close()

        #if stokes use: initializeSolution(std::string savePrefix, int fieldPolyOrder, int delta_k = 1, FunctionPtr forcingFunction = Teuchos::null);
        #if NS use: NavierStokesVGPFormulation(std::string prefixString, int spaceDim, double Re, int fieldPolyOrder, int delta_k = 1, FunctionPtr forcingFunction = Teuchos::null, bool transientFormulation = false, bool useConformingTraces = false);
        if self.stringList.eq_type == "Stokes":
            self.form.initializeSolution(fileName, self.stringList[1])
        elif self.stringList.eq_type == "Navier-Stokes":
            self.form.NavierStokesVGPFormulation(fileName, self.stringList[3], self.stringList[1], self.stringList[5])




    def plot(self, pltstr):
        """
        if (pltstr == "u1"):
            return plotter.plotU1(self.form)
        elif (pltstr == "u2"):
            return plotter.plotU2(self.form)
        elif (pltstr == "p"):
            return plotter.plotP(self.form)
        elif (pltstr == "stream"):
            return plotter.plotStream(self.form)
        elif (pltstr == "mesh"):
            return plotter.plotMesh(self.form)
        elif (pltstr == "error"):
            return plotter.plotError(self.form, self.stringList[0] == "Navier-Stokes")
        """

        return random.choice(self.puppies)
        
         

    
