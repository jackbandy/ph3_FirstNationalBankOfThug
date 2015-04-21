from FormCreator import *
import unittest
from PyCamellia import *

class FormCreatorTest(unittest.TestCase):
    #test the making of a Navier Stokes Formulation
    def test_Navier(self):
        c = FormCreator();
        inflows = [SpatialFilter.matchingX(1), SpatialFilter.matchingY(1)]
        x_vels = [Function.constant(5), Function.constant(1)]
        y_vels = [Function.constant(6), Function.constant(3)]
        outflows = [SpatialFilter.matchingX(4), SpatialFilter.matchingY(4)]
        dims = [1.0, 1.0]
        elems = [2,2]
        form = c.main(3, inflows, x_vels, y_vels, outflows, dims, elems, 800.0, False)
        

if __name__ == '__main__':
    unittest.main()
