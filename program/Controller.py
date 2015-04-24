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
    #   String List inflowPos
    #   String List inflowFunctions
    #   String List outflowPos
    #   
    def solve(self, eq_type, pOrder, transOrSteady, dimensions, meshElements, reyNum, inflowPos, inflowFunctions, outflowPos):
        self.stringList = [eq_type,
                           pOrder,
                           transOrSteady,
                           dimensions,
                           meshElements,
                           reyNum,
                           inflowPos,
                           inflowFunctions,
                           outflowPos]
        eq_type_ = eq_type
        pOrder_ = int(eq_type)
        transOrSteady_ = transOrSteady
        dimensions_ = (float(dimensons[0]), float(dimensions[1]))
        meshElements_ = (int(meshElements[0]), int(meshElements[1]))
        reyNum_ = int(reyNum)
        inflowPos_ 
        inflowFunctions_ = []
        for x in inflowFunctions:
            inflowFunctions_.append(self.interpreter2.interpret(x))        
        outflowPos_
        
    def save(self, fileName):
        #saving stringlist
        file = open(fileName, 'wb')
        pickle.dump(stringList, file)
        file.close

        #saving form solution
        form.solution().save(fileName)

    def load(self, fileName):
        #loading stringlist
        file = open(fileName, 'rb')
        stringList = pickle.load(file)
        file.close()

    def plot(self, pltstr):
        return random.choice(self.puppies)
        #loading solution
        #if stokes use:  void initializeSolution(std::string savePrefix, int fieldPolyOrder, int delta_k = 1, FunctionPtr forcingFunction = Teuchos::null);
        #if NS use: NavierStokesVGPFormulation(std::string prefixString, int spaceDim, double Re, int fieldPolyOrder, int delta_k = 1, FunctionPtr forcingFunction = Teuchos::null, bool transientFormulation = false, bool useConformingTraces = false);

    
