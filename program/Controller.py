import Interpreter2


class Controller(object):

    def __init__(self):
        self.stringList = []
        self.form = None
        self.interpreter2 = Interpreter2.Interpreter2()
    
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
        for x as inflowFunctions:
            inflowFunctions_.append(self.interpreter2.interpret(x))        
        outflowPos_
        
        

    
