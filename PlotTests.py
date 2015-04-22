# PlotTests.py
# Jack Bandy

import unittest
import plotter
from plotter import *
from PyCamellia import *
from FormCreator import *


class PlotTests(unittest.TestCase):
  '''Test Things'''

  plter = plotter()
  c = FormCreator()
  inflows = [SpatialFilter.matchingX(6), SpatialFilter.matchingY(7)]
  x_vels = [Function.constant(5), Function.constant(1)]
  y_vels = [Function.constant(6), Function.constant(3)]
  outflows = [SpatialFilter.matchingX(4), SpatialFilter.matchingY(4)]
  dims = [8.0, 8.0]
  elems = [4,4]
  form = c.main(3, inflows, x_vels, y_vels, outflows, dims, elems)

#  def testu1(self):
#    self.plter.plotU1(self.form)
#  def testu2(self):
#    self.plter.plotU2(self.form)
#  def testp(self):
#    self.plter.plotP(self.form)
#  def teststream(self):
#    self.plter.plotStream(self.form)
  def testmesh(self):
    self.plter.plotMesh(self.form)
#  def testerror(self):
#    self.plter.plotError(self.form,True)

# Run the tests:
if (__name__ == '__main__'):
  unittest.main()
