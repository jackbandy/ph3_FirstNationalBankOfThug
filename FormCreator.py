from PyCamellia import *
from string import *
import os

#takes the inputs from the GUI and returns a formulation with all conditions attached
class FormCreator():
    def __init__(self):
        pass
    #@return
    #poly - an integer between 1 and 9
    #inflows - an array of spacial filters
    #x_vels - an array of Functions for the x velocities mapping to inflows of the same array index
    #y_vels - an array of Functions for the y velocities mapping to inflows of the same array index
    #outflows - an array of spacial filters
    #dims - the dimensions of the mesh; a list of doubles of length 2
    #elems - a list of ints; the elements in the mesh
    #re - renolds number, a double, optional argument
    #transient - Boolean, whether or not the function is transient
    def main(self, poly, inflows, x_vels, y_vels, outflows, dims, elems, re=None, transient=False):
        delta_k = 1 
        space_dim = 2
        mesh = self.makeMesh(dims, elems)

        #for Navier
        if re != None:
            form = NavierStokesVGPFormulation(mesh, re, poly, delta_k)
    
    #for Stokes
        else:
            #self.context.setNav(False)
            use_conforming_traces = True
            mu = 1.0
            form = StokesVGPFormulation(space_dim, use_conforming_traces, mu, transient)
            form.initializeSolution(mesh, poly, delta_k)
        
        form.addZeroMeanPressureCondition()

        #adding conditions
        inflow = self.add_inflow_conditions(form, transient, inflows, x_vels, y_vels)
        outflow = self.add_outflow_conditions(form, outflows)
        #self.add_conditions("wall", form, transient)
        form.addWallCondition(self.implicit_walls(dims, inflow, outflow))
        
        
        return form

        


        
        #if not loading from a file make a new mesh Topology
        #if not self.context.loaded:
    def makeMesh(self, dims, elems):
        x0 = [0., 0.]
        return MeshFactory.rectilinearMeshTopology(dims, elems, x0)
            


       


    #adds wall/inflow/outflow conditions to the form
    def add_inflow_conditions(self, form, transient, inflows, x_vels, y_vels):
        total_boundary = SpatialFilter.negatedFilter(SpatialFilter.allSpace())
        for x in range(0, inflows.__len__()):
            velocity = self.get_velocity(transient, form, x_vels[x], y_vels[x])
            form.addInflowCondition(inflows[x], velocity)
            total_boundary = SpatialFilter.unionFilter(total_boundary, inflows[x])
        return total_boundary

    #adds wall/inflow/outflow conditions to the form
    def add_outflow_conditions(self, form, outflows):
        total_boundary = SpatialFilter.negatedFilter(SpatialFilter.allSpace())
        for boundary in outflows:
            form.addOutflowCondition(boundary)
            total_boundary = SpatialFilter.unionFilter(total_boundary, boundary)
        return total_boundary

    #adds wall conditions on all part of perameter that is not an inflow or outflow
    def implicit_walls(self, dimensions, inflow, outflow):
        flows = SpatialFilter.unionFilter(inflow, outflow)
        wallConditions = SpatialFilter.negatedFilter(flows)
        return wallConditions

    #prototype
    def get_velocity(self, transient, form, x_vel, y_vel):
        topVelocity = Function.vectorize(x_vel, y_vel)
        if transient:
            timeRamp = TimeRamp.timeRamp(form.getTimeFunction(),1.0)
            topVelocity = topVelocity*timeRamp
        return topVelocity
    
        
    #takes a string and returns a spacial filter
    #unused for phase 3
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
