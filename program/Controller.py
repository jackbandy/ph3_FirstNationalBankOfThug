from PyCamellia import *
import Interpreter2
import pickle
import random
import plotter
import re

class Controller(object):

    def __init__(self):
        self.stringList = []
        self.form = None
        self.refinementNumber = 0
        self.plotter = plotter.plotter()
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
        pOrder_ = int(pOrder)
        state_ = state
        dimensions_ = (float(dimensions[0]), float(dimensions[1]))
        meshElements_ = (int(meshElements[0]), int(meshElements[1]))
        reyNum_ = int(reyNum)
        inflowPos_ = []
        inflowSpatialFilters_ = []
        for x in inflow:
            inflowSpatialFilters_.append(self.parsePos(x[0]))
            inflowFunctions_.append((self.interpreter2.interpret(x[1]), self.interpreter2.interpret(x[2])))
        outflowSpatialFilters_ = []
        for x in outflow:
            outflowSpatialFilters_.append(self.parsePos(x))


        #Get a form with FormCreator - Woodson?

        #TEST
        spaceDim = 2
        Re = 800.0
        dims = [8.0,2.0]
        numElements = [8,2]
        x0 = [0.,0.]
        meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
        polyOrder = 3
        delta_k = 1
        self.form = NavierStokesVGPFormulation(meshTopo,Re,polyOrder,delta_k)
        self.stringList = ["Navier-Stokes", polyOrder, "steady", dims, numElements, Re]

        #Solve
        if eq_type == "Navier-Stokes":
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

        toRet =  "Initial mesh has %i elements and %i degrees of freedom." % (mesh.numActiveElements(), mesh.numGlobalDofs())
        toRet = toRet + "Energy error after %i refinements: %0.3f" % (self.refinementNumber, energy)
        return toRet



    #Returns a spatial filter given a string that is 
    def parsePos(self, input):
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


    def manualRefine(hOrP, elements):
        pass
    
    
    def autoRefine(hOrP):
        pass


        
    def save(self, fileName):
        if (self.form != None):
            #saving stringlist and refinement #
            file = open(fileName, 'wb')
            pickle.dump(self.stringList, file)
            #pickle.dump(refinement#, file)
            file.close()
            #saving form solution
            self.form.solution().save(fileName)
        else:
            raise Exception

    def load(self, fileName):
        try:
            #loading stringlist and refinement #
            file = open(fileName, 'rb')
            self.stringList = pickle.load(file)
            #self.refinement# = pickle.load(file)
            file.close()
            #if stokes use: initializeSolution(std::string savePrefix, int fieldPolyOrder, int delta_k = 1, FunctionPtr forcingFunction = Teuchos::null);
            if self.stringList.eq_type == "Stokes":
                self.form.initializeSolution(fileName, self.stringList[1])
            #if NS use: NavierStokesVGPFormulation(std::string prefixString, int spaceDim, double Re, int fieldPolyOrder, int delta_k = 1, FunctionPtr forcingFunction = Teuchos::null, bool transientFormulation = false, bool useConformingTraces = false);
            elif self.stringList.eq_type == "Navier-Stokes":
                self.form = NavierStokesVGPFormulation(fileName, 2, self.stringList[5], self.stringList[1])
        except Exception:
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
            return self.plotter.plotError(self.form, self.stringList[0] == "Navier-Stokes")

        return random.choice(self.puppies)
        
         

    
