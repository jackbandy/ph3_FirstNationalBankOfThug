from PyCamellia import *
import matplotlib.pyplot as plt
import numpy as np
import sys
import matplotlib.animation as animation
plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'

spaceDim = 2
useConformingTraces = True
mu = 1.0
form = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
dims = [1.0,1.0]
numElements = [2,2]
x0 = [0.,0.]
meshTopo = MeshFactory.rectilinearMeshTopology(dims,numElements,x0)
polyOrder = 3
delta_k = 1

form.initializeSolution(meshTopo,polyOrder,delta_k)

form.addZeroMeanPressureCondition()

topBoundary = SpatialFilter.matchingY(1.0)
notTopBoundary = SpatialFilter.negatedFilter(topBoundary)

x = Function.xn(1)
rampWidth = 1./64
H_left = Function.heaviside(rampWidth)
H_right = Function.heaviside(1.0-rampWidth);
ramp = (1-H_right) * H_left + (1./rampWidth) * (1-H_left) * x + (1./rampWidth) * H_right * (1-x)

zero = Function.constant(0)
topVelocity = Function.vectorize(ramp,zero)

form.addWallCondition(notTopBoundary)
form.addInflowCondition(topBoundary,topVelocity)

refinementNumber = 0
form.solve()

mesh = form.solution().mesh();

energyError = form.solution().energyErrorTotal()
elementCount = mesh.numActiveElements()
globalDofCount = mesh.numGlobalDofs()
print("Initial mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))
print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))

threshold = .05
while energyError > threshold and refinementNumber <= 1:
  form.hRefine()
  form.solve()
  energyError = form.solution().energyErrorTotal()
  refinementNumber += 1
  elementCount = mesh.numActiveElements()
  globalDofCount = mesh.numGlobalDofs()
  print("Energy error after %i refinements: %0.3f" % (refinementNumber, energyError))
  print("Mesh has %i elements and %i degrees of freedom." % (elementCount, globalDofCount))

# print out per-cell energy error for cells with energy error > 0.01:
perCellError = form.solution().energyErrorPerCell()
for cellID in perCellError:
  if perCellError[cellID] > .01:
    print("Energy error for cell %i: %0.3f" % (cellID, perCellError[cellID]))

savePrefix = "stokesExample"
print ("Saving to " + savePrefix)
form.save(savePrefix)
print ("...saved.")

print ("Loading saved solution...")
loadedForm = StokesVGPFormulation(spaceDim,useConformingTraces,mu)
loadedForm.initializeSolution(savePrefix,polyOrder,delta_k)
print ("Loaded.")

exporter = HDF5Exporter(form.solution().mesh(), "steadyStokes", ".")
exporter.exportSolution(form.solution(),0)

transient = True
dt = 0.2
totalTime = 2.0
numTimeSteps = int(totalTime / dt)
transientForm = StokesVGPFormulation(spaceDim,useConformingTraces,mu,transient,dt)

timeRamp = TimeRamp.timeRamp(transientForm.getTimeFunction(),1.0)

transientForm.initializeSolution(meshTopo,polyOrder,delta_k)

transientForm.addZeroMeanPressureCondition()
transientForm.addWallCondition(notTopBoundary)
transientForm.addInflowCondition(topBoundary,timeRamp * topVelocity)

transientExporter = HDF5Exporter(transientForm.solution().mesh(), "transientStokes", ".")

ims = []
graphint = 0
setBounds = False

for timeStepNumber in range(numTimeSteps):
  transientForm.solve()
  transientExporter.exportSolution(transientForm.solution(),transientForm.getTime())
  transientForm.takeTimeStep()

  print("Time step %i completed" % timeStepNumber)
  u1_soln = Function.solution(transientForm.u(1),transientForm.solution())
#  u1_soln = Function.solution(form.u(2),form.solution())
  
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
  for cellID in activeCellIDs:
    vertices = mesh.verticesForCell(cellID)
    xMinLocal = vertices[0][0]
    xMaxLocal = vertices[1][0]
    yMinLocal = vertices[0][1]
    yMaxLocal = vertices[2][1]
    xMin = sys.float_info.max
    xMax = sys.float_info.min
    yMin = sys.float_info.max
    yMax = sys.float_info.min
    (values,points) = u1_soln.getCellValues(mesh,cellID,refCellVertexPoints)
    zValues = np.array(values)
    zValues = zValues.reshape((num_x,num_y)) # 2D array
    if(setBounds is False):
#      zMin = (zValues.min())
#      zMax = (zValues.max())
      zMin = -.75
      zMax = .75
      setBounds = True
    zList.append((zValues,(xMinLocal,xMaxLocal),(yMinLocal,yMaxLocal)))
    xMin = min(xMinLocal,xMin)
    xMax = max(xMaxLocal,xMax)
    yMin = min(yMinLocal,yMin)
    yMax = max(yMaxLocal,yMax)
  for zTuple in zList:
    zValues,(xMinLocal,xMaxLocal),(yMinLocal,yMaxLocal) = zTuple
#    if graphint % 2 == 0:
    im = plt.imshow(zValues, cmap='coolwarm', vmin=zMin, vmax=zMax,
                 extent=[xMinLocal, xMaxLocal, yMinLocal, yMaxLocal],
                 interpolation='bicubic', origin='lower')
#    else:
#      im = plt.imshow(zValues, cmap='BrBG', vmin=zMin, vmax=zMax,
#                 extent=[xMinLocal, xMaxLocal, yMinLocal, yMaxLocal],
#                 interpolation='bicubic', origin='lower')
#  graphint = graphint + 1
  ims.append([im])
  print("added img")



fig = plt.figure()
ani = animation.ArtistAnimation(fig, ims, interval=500, blit=True,
    repeat_delay=500)

myWriter = animation.FFMpegWriter()
ani.save('anim.mp4', writer=myWriter)
plt.show()



