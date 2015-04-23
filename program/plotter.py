
from PyCamellia import *

import matplotlib.pyplot as plt
import numpy as np
import sys


class Plotter:
    def plotU1(form)
	mesh = form.solution().mesh()
	soln = Function.solution(form.u(1),form.solution())
	plotFunction(soln,mesh,"u1")
    def plotU2(form):
	mesh = form.solution().mesh()
	soln = Function.solution(form.u(2),form.solution()) 
	plotFunction(soln,mesh,"u2")
    def plotP(form):
	mesh = form.solution().mesh()
	soln = Function.solution(form.p,form.solution()) 
	plotFunction(soln,mesh,"p")
    def plotStream(form):
	stream = form.streamSolution()
	stream.solve()
	mesh = stream.mesh()
	soln = Function.solution(form.streamPhi(),stream) 
	plotFunction(soln,mesh,"Stream")
    def plotMesh(form):
	#TODO
    def plotError(form,stokes):
	if stokes:
	   error = form.solution().energyErrorPerCell()
	else:
	   error = form.solutionIncrement().energyErrorPerCell()
	num_x = 10
	num_y = 10
	
	
	zList = [] # should have tuples (zVals, (x_min,x_max), (y_min,y_max)) -- one for each cell
	activeCellIDs = mesh.getActiveCellIDs()
	xMin = sys.float_info.max
	xMax = sys.float_info.min
	yMin = sys.float_info.max
	yMax = sys.float_info.min
	zMin = sys.float_info.max
	zMax = sys.float_info.min
	for cellID in activeCellIDs:
	  vertices = mesh.verticesForCell(cellID)
	  xMinLocal = vertices[0][0]
	  xMaxLocal = vertices[1][0]
	  yMinLocal = vertices[0][1]
	  yMaxLocal = vertices[2][1]
	  values = []
	  for x in range(0,100):
	     values.append(error[cellID])
	  zValues = np.array(values) 
	  zValues = zValues.reshape((num_x,num_y)) # 2D array
	  zMin = min(zValues.min(),zMin)
	  zMax = max(zValues.max(),zMax)
	  zList.append((zValues,(xMinLocal,xMaxLocal),(yMinLocal,yMaxLocal)))
	  xMin = min(xMinLocal,xMin)
	  xMax = max(xMaxLocal,xMax)
	  yMin = min(yMinLocal,yMin)
	  yMax = max(yMaxLocal,yMax)
	
	#plot them
	for zTuple in zList:
	  zValues,(xMinLocal,xMaxLocal),(yMinLocal,yMaxLocal) = zTuple
	  plt.imshow(zValues, cmap='coolwarm', vmin=zMin, vmax=zMax,
	           extent=[xMinLocal, xMaxLocal, yMinLocal, yMaxLocal],
	           interpolation='bicubic', origin='lower')
	plt.title('cavity flow error')
	plt.colorbar()
	plt.axis([xMin, xMax, yMin, yMax])
	return plt.saveFig("plot")

    def plotFunction(soln, mesh, title):
	num_x = 10
	num_y = 10
	refCellVertexPoints = []
	
	for j in range(num_y):
	  y = -1 + 2. * float(j) / float(num_y - 1) # go from -1 to 1
	  for i in range(num_x):
	    x = -1 + 2. * float(i) / float(num_x - 1) # go from -1 to 1
	    refCellVertexPoints.append([x,y])
	
	zList = [] # should have tuples (zVals, (x_min,x_max), (y_min,y_max)) -- one for each cell
	activeCellIDs = mesh.getActiveCellIDs()
	xMin = sys.float_info.max
	xMax = sys.float_info.min
	yMin = sys.float_info.max
	yMax = sys.float_info.min
	zMin = sys.float_info.max
	zMax = sys.float_info.min
	for cellID in activeCellIDs:
	  vertices = mesh.verticesForCell(cellID)
	  xMinLocal = vertices[0][0]
	  xMaxLocal = vertices[1][0]
	  yMinLocal = vertices[0][1]
	  yMaxLocal = vertices[2][1]
	  (values,points) = soln.getCellValues(mesh,cellID,refCellVertexPoints)
	  zValues = np.array(values) 
	  zValues = zValues.reshape((num_x,num_y)) # 2D array
	  zMin = min(zValues.min(),zMin)
	  zMax = max(zValues.max(),zMax)
	  zList.append((zValues,(xMinLocal,xMaxLocal),(yMinLocal,yMaxLocal)))
	  xMin = min(xMinLocal,xMin)
	  xMax = max(xMaxLocal,xMax)
	  yMin = min(yMinLocal,yMin)
	  yMax = max(yMaxLocal,yMax)
	
	#plot them
	for zTuple in zList:
	  zValues,(xMinLocal,xMaxLocal),(yMinLocal,yMaxLocal) = zTuple
	  plt.imshow(zValues, cmap='coolwarm', vmin=zMin, vmax=zMax,
	           extent=[xMinLocal, xMaxLocal, yMinLocal, yMaxLocal],
	           interpolation='bicubic', origin='lower')
	
	plt.title(title)
	plt.colorbar()
	plt.axis([xMin, xMax, yMin, yMax])
	return plt.savefig("plot") # will save a plot to disk
	