from PyCamellia import *
from State import *
from PostSolve import *
from string import *
import os

#takes the inputs from the GUI and returns a formulation with all conditions attached
class FormCreator(State):

    def __init__(self, poly, inflows, inflow_x_vels, inflow_y_vels, outflows,  dims, elems,re=None, transient=False):
        delta_k = 1 
        space_dim = 2
        mesh = self.makeMesh(dims, elems)

        #for unloaded Navier
        if re != None:
            form = NavierStokesVGPFormulation(mesh, re, poly, delta_k)
    
    #for unloaded Stokes
        else:
            #self.context.setNav(False)
            use_conforming_traces = False
            mu = 1.0
            transient = self.is_transient()
            form = StokesVGPFormulation(space_dim, use_conforming_traces, mu, transient)
            """if self.context.loaded:
                form.initializeSolution(self.context.file_name, poly_order)
            else:"""
            form.initializeSolution(mesh, poly, delta_k)
            form.addZeroMeanPressureCondition()

        #adding conditions
        inflow = self.add_inflow_conditions(form, transient, inflows, inflow_x_vels, inflow_y_vels)
        outflow = self.add_outflow_conditions(form, outflows)
        #self.add_conditions("wall", form, transient)
        form.addWallCondition(self.implicit_walls(dimensions, inflow, outflow))


        
        #if not loading from a file make a new mesh Topology
        #if not self.context.loaded:
        def makeMesh(self, dims, elems):
            x0 = [0., 0.]
            return MeshFactory.rectilinearMeshTopology(dims, elems, x0)

            #if self.loaded:
                #NavierStokesVGPFormulation(self.context.file_name, space_dim, re, poly_order)
            


    """
    No idea what this is

        #solves and prints result
        if is_Navier:
            nonlinearThreshold = 1e-3
            maxSteps = 10
            normOfIncrement = 1
            stepNumber = 0
            while normOfIncrement > nonlinearThreshold and stepNumber < maxSteps:
                form.solveAndAccumulate()
                normOfIncrement = form.L2NormSolutionIncrement()
                stepNumber += 1
            mesh = form.solution().mesh()
            energy = form.solutionIncrement().energyErrorTotal()
            self.context.printRefine(energy, mesh)

        else:
            form.solve()
            mesh = form.solution().mesh()
            energy = form.solution().energyErrorTotal()
            self.context.printRefine(energy, mesh)
<<<<<<< HEAD
   """

"""
>>>>>>> 39f0eb5896dfa5869ae44023ce8842b3ccba2662
       





    #adds wall/inflow/outflow conditions to the form
    def add_inflow_conditions(self, form, transient, inflows, x_vels, y_vels):
        total_boundary = SpatialFilter.negatedFilter(SpatialFilter.allSpace())
        for x in range(0, inflows.__len__()):
            velocity = self.get_velocity(transient, form, x_vels[x], y_vels[x])
            form.addInflowCondition(inflows[x], velocity)
            total_boundary = SpatialFilter.unionFilter(total_boundary, boundary)
        return total_boundary

    #adds wall/inflow/outflow conditions to the form
    def add_outflow_conditions(self, form, outflows):
        total_boundary = SpatialFilter.negatedFilter(SpatialFilter.allSpace())
        for boundary in outflows:
            form.addOutflowCondition(boundary)
            total_boundary = SpatialFilter.unionFilter(total_boundary, boundary)
        return total_boundary

    def implicit_walls(self, dimensions, inflow, outflow):
        flows = SpatialFilter.unionFilter(inflow, outflow)
        x = dimensions[0]
        y = dimensions[1]
        leftWall = SpatialFilter.intersectionFilter(SpatialFilter.intersectionFilter(SpatialFilter.matchingX(0), SpatialFilter.lessThanY(y)), SpatialFilter.greaterThanY(0))
        rightWall = SpatialFilter.intersectionFilter(SpatialFilter.intersectionFilter(SpatialFilter.matchingX(x), SpatialFilter.lessThanY(y)), SpatialFilter.greaterThanY(0))
        topWall = SpatialFilter.intersectionFilter(SpatialFilter.intersectionFilter(SpatialFilter.matchingY(y), SpatialFilter.lessThanX(x)),SpatialFilter.greaterThanX(0))
        bottumWall = SpatialFilter.intersectionFilter(SpatialFilter.intersectionFilter(SpatialFilter.matchingY(0), SpatialFilter.lessThanX(x)), SpatialFilter.greaterThanX(0))
        perimeter = SpatialFilter.unionFilter(SpatialFilter.unionFilter(SpatialFilter.unionFilter(leftWall, rightWall), bottumWall), topWall)
        wallConditions = SpatialFilter.unionFilter(perimeter, SpatialFilter.negatedFilter(flows)) 
        return wallConditions

    #prototype
    def get_velocity(self, transient, form, x_vel, y_vel):
        interp = Interpreter2()
        xVelocity = interp.interpret(x_vel)
        yVelocity = interp.interpret(y_vel)
        topVelocity = Function.vectorize(xVelocity,yVelocity)
        if transient:
            timeRamp = TimeRamp.timeRamp(form.getTimeFunction(),1.0)
            topVelocity = topVelocity*timeRamp
        return topVelocity
    
    def get_velocity(self, string):
        interp = Interpreter2()
	try:
        	x = interp.interpret(string)
    	except NameError:
        	print("Input Error")
    	return x 
        
    #takes a string and returns a spacial filter
    def get_space_fil(self, prompt):
        answer = self.context.query(prompt)
        altered = answer.lower()
        altered = altered.translate(None, whitespace)#remove whitespace
        try:
        	if altered.find(",") > -1: #if there are multiple spacial filters
        	    halves = altered.split(",")#split them
        	    filter1 = self.get_space_fil_helper(halves[0],prompt)
        	    filter2 = self.get_space_fil_helper(halves[1],prompt)
        	    return SpatialFilter.intersectionFilter(filter1, filter2)
        	else:
            		return self.get_space_fil_helper(altered, prompt)
        except ValueError:
        	self.context.parse_error(answer)
        	self.get_space_fil(prompt)


    #space_fil's helper method
    def get_space_fil_helper(self, assignment, prompt):
        is_x =  assignment.find("x") > -1
        if not is_x:
            if assignment.find("y") == -1:
                self.context.parse_error(assignment)
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
            self.context.parse_error(assignment)
            answer = self.context.query("Please input spatial filter in form x=3, y< 4")
            return self.get_space_fil_helper(answer, prompt)
"""
