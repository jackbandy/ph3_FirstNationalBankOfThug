from PyCamellia import *
import Interpreter2
import pickle
import random

class Controller(object):

    def __init__(self):
        self.stringList = []
        self.form = None
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
        self.stringList = [eq_type,
                           pOrder,
                           state,
                           dimensions,
                           meshElements,
                           reyNum,
                           inflow,
                           outflow]
        eq_type_ = eq_type
        pOrder_ = int(eq_type)
        state_ = state
        dimensions_ = (float(dimensons[0]), float(dimensions[1]))
        meshElements_ = (int(meshElements[0]), int(meshElements[1]))
        reyNum_ = int(reyNum)
        inflowPos_ = []
        inflowFunctions_ = []
        for x in inflowFunctions:
            inflowPos_.append(x[0])
            inflowFunctions_.append(self.interpreter2.interpret(x[1]))
        inflowSpatialFilter_ = parsePos(inflowPos_)
        
        outflowPos_ = []
        for x in outflow:
            outflowPos_.append(self.interpreter2.interpret(x))        
        outflowPos_

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
        #loading solution
        #if stokes use: initializeSolution(std::string savePrefix, int fieldPolyOrder, int delta_k = 1, FunctionPtr forcingFunction = Teuchos::null);
        if self.stringList.eq_type == "Stokes":
            self.form.initializeSolution(fileName, self.stringList[1])
        #if NS use: NavierStokesVGPFormulation(std::string prefixString, int spaceDim, double Re, int fieldPolyOrder, int delta_k = 1, FunctionPtr forcingFunction = Teuchos::null, bool transientFormulation = false, bool useConformingTraces = false);
        elif self.stringList.eq_type == "Navier-Stokes":
            self.form.NavierStokesVGPFormulation(fileName, self.stringList[3], self.stringList[1], self.stringList[5]) 

    
