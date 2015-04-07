from PyCamellia import *
from State import *
from PostSolve import *
from string import *
import os

#takes the inputs from the GUI and returns a formulation with all conditions attached
class FormCreator(State):

    #constructor for Navier
    def __init__(self, dims, elems, poly, inflows, inflow_vels, outflows):
        self.is_Navier = True
        self.mesh = self.makeMesh(dims, elems)
        delta_k = 1
        space_dim = 2
        form = NavierStokesVGPFormulation(meshTopo, re, poly_order, delta_k)
        self.add_inflows(form, inflows, inflow_vels)
        self.add_outflows(form, outflows)
        
    
    #constructor for Stokes
    def __init__(self, re, dims, elems, poly, inflows, inflow_vels, outflows):
        self.is_Navier = False
        self.re = re
        self.mesh = self.makeMesh(dims, elems)

    #Constructor for Navier Loaded
    def __init__(self, poly, poly, inflows, inflow_vels, outflows):

    #constructor for Stokes Loaded


        
        #if not loading from a file make a new mesh Topology
        #if not self.context.loaded:
        def makeMesh(self, dims, elems):
            x0 = [0., 0.]
            return MeshFactory.rectilinearMeshTopology(dims, elems, x0)

  #Process for constructing the forumla
        poly_order = self.get_poly()
        delta_k = 1 #what is this? look at RefCellPointsExampl.py
        space_dim = 2
        transient = False
        if is_Navier:
            self.context.setNav(True)
            if self.context.loaded:
                NavierStokesVGPFormulation(self.context.file_name, space_dim, re, poly_order)
            else:
                form = NavierStokesVGPFormulation(meshTopo, re, poly_order, delta_k)
                transient = False
        else: #stokes
            self.context.setNav(False)
            use_conforming_traces = False
            mu = 1.0
            transient = self.is_transient()
            form = StokesVGPFormulation(space_dim, use_conforming_traces, mu, transient)
            if self.context.loaded:
                form.initializeSolution(self.context.file_name, poly_order)
            else:
                form.initializeSolution(meshTopo, poly_order, delta_k)
        form.addZeroMeanPressureCondition() #what is this? look at RefCellPointsExampl.py

        #adding conditions
        inflow = self.add_conditions("inflow", form, transient)
        outflow = self.add_conditions("outflow", form, transient)
        #self.add_conditions("wall", form, transient)
        form.addWallCondition(self.implicit_walls(dimensions, inflow, outflow))

        #solves and prints result
        print("solving...\n")
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
       
        
        #switch states
        self.context.switch_state(PostSolve(self.context, form))
        #control flow back to context

    def get_poly(self):
        poly_order = self.parse_int("What polynomial order? (1 to 9)\n")
        if poly_order > 0 and poly_order < 10:
            return poly_order
        else:
            print(str(poly_order) + " is not between 1 and 9")
            return self.get_poly()


#decides whether the formula is Stokes or Navier-Stokes
    def get_form(self):
        answer = self.context.query("Would you like to solve Stokes or Navier-Stokes?\n")
        altered = answer.lower()
        if altered in ("stokes","s","rolling stokes") :
            return False
        elif altered in ("navier-stokes","navier","nav","navi","n-s", "navier stokes", "navierstokes") :
            return True
        else:
            self.context.parse_error(answer)
            return self.get_form()

    #gives the user a prompt and returns an int
    def parse_int(self, prompt):
        answer = self.context.query(prompt)
        if (prompt == "What Reynolds number?\n"):
            try:
                altered =  int(answer)
                if (altered < 0):
                    self.context.parse_error(answer)
                    print("Must be positive")
                    return self.parse_int(prompt)
                else:
                    return altered
            except ValueError:
                self.context.parse_error(answer)
                return self.parse_int(prompt)
        try:
            altered =  int(answer)
            return altered
        except ValueError:
            self.context.parse_error(answer)
            return self.parse_int(prompt)

    def is_transient(self):
        answer = self.context.query("Transient or steady state?\n")
        altered = answer.lower()
        if altered == "transient" :
            return True
        elif altered == "steady" or altered == "steady state" or altered == "steadystate":
            return False
        else:
            self.context.parse_error(answer)
            return self.is_transient()

    #gives the user a prompt and returns a tuple of floats
    def get_dimensions(self):
        answer = self.context.query("This solver handles rectangular meshes with lower-left corner at the origin. What are the dimensions of your mesh? (e.g., 1.0 x 2.0)\n")
        altered = answer.translate(None, whitespace)
        altered = altered.lower()
        halves = altered.split("x")
        if(len(halves) < 2):
            self.context.parse_error(answer)
            print("Did not receive two floats")
            return self.get_dimensions()
        try:
            #type error here
            if (not (float(halves[0]) >  0) or not(float(halves[1]) > 0)):
                self.context.parse_error(answer)
                print("Needs each dimension to be greater than 0")
                return self.get_dimensions()
            else:
                return [float(halves[0]), float(halves[1])]#strings to floats
        except ValueError:
            self.context.parse_error(answer)
            return self.get_dimensions()

    #gives the user a prompt and returns a tuple of ints
    def get_elements(self):
        answer = self.context.take_user_input("How many elements in the initial mesh? (E.g. 3 x 5)\n")
        altered = answer.translate(None, whitespace)
        altered = altered.lower()
        halves = altered.split("x")
        if(len(halves) < 2):
            self.context.parse_error(answer)
            print("Did not have two ints")
            return self.get_elements()

        try:
            if (not(int(halves[0]) > 0) or not(int(halves[1]) > 0)):
                self.context.parse_error(answer)
                print("Needs each dimension to be at least 1")
                return self.get_elements()
            else:
                return [int(halves[0]), int(halves[1])]
        except ValueError:
            self.context.parse_error(answer)
            return self.get_elements()

    #adds wall/inflow/outflow conditions to the form
    def add_conditions(self, condition, form, transient):
        number = self.parse_int("How many " + condition + " conditions?\n")
        total_boundary = SpatialFilter.negatedFilter(SpatialFilter.allSpace())
        for n in range(0, number):
            boundary = self.get_space_fil("For " + condition + " condition " + str(n+1) + ", what region of space? (E.g. x=0.5, y > 3)\n")
            if condition == "inflow": #calculate velocity if inflow
                velocity = self.get_velocity(n, transient, form)
                form.addInflowCondition(boundary, velocity)
            elif condition == "outflow":
                form.addOutflowCondition(boundary)
            else:
                assert condition == "wall"
                form.addWallCondition(boundary)
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
    def get_velocity(self, number, transient, form):
        xVelocity = self.get_x_velocity(number)
        yVelocity = self.get_y_velocity(number)
        topVelocity = Function.vectorize(xVelocity,yVelocity)
        if transient:
            timeRamp = TimeRamp.timeRamp(form.getTimeFunction(),1.0)
            topVelocity = topVelocity*timeRamp
        return topVelocity
    
    def get_x_velocity(self, number):
        interp = Interpreter2()
        xVelocity = self.context.query("For inflow condition " + str(number+1) + ", what is the x component of the velocity?\n")
	try:
        	x = interp.interpret(xVelocity)
    	except NameError:
        	print("Input Error")
        	x = self.get_x_velocity(number)
    	return x 

    def get_y_velocity(self, number):
        interp = Interpreter2()
        yVelocity = self.context.query("For inflow condition " + str(number+1) + ", what is the y component of the velocity?\n")
	try:
        	y = interp.interpret(yVelocity)
    	except NameError:
        	print("Input Error")
        	y = self.get_y_velocity(number)
    	return y
        
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
