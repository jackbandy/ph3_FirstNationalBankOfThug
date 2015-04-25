from PyCamellia import *
from State import *
from Context import *
import Creation
from string import *
#import Plotter

class PostSolve(State):
    def __init__(self, context, form):
        self.context = context
	self.form = form

    #this method talks to the user, giving the user her options
    def main(self):
        user_input = self.context.take_user_input("You can now: plot, refine, save, load, error (shows error in cells) or exit.\n")
        user_input = user_input.lower()
	words = user_input.split()
	
	if (len(words) > 1):
	    phrase = words[1:]
	else:
	    phrase = []
	
        if (words[0] == "plot"):
            self.plot(phrase)
        elif (words[0] == "refine"):
            self.refine(phrase)
        elif (words[0] == "save"):
            self.save(phrase)
        elif(words[0] == "load"):
            self.load(phrase)
        elif (words[0] == "exit"):
            self.context.terminate = True
        elif (words[0] == "error"):
            self.display_error()
        else:
            self.context.parse_error(user_input)
            self.main()

    #creates a graph of the current function
    def plot(self, phrase):
        if (len(phrase) > 0):
            user_input = phrase[0]
            
        else:
            user_input = self.context.take_user_input("What would you like to plot? (u1, u2, p, stream, mesh, error)\n")

	if (user_input == "u1"):
	    soln =  Function.solution(self.form.u(1),self.form.solution())
	elif (user_input == "u2"):
	    soln = Function.solution(self.form.u(2),self.form.solution())
	elif (user_input == "p"):
	    soln = Function.solution(self.form.p(),self.form.solution())
	elif (user_input == "stream"):
	    soln = Function.solution(self.form.streamPhi(),self.form.solution())
	elif (user_input == "mesh"):
            plotter.makeGrid(mesh)
	elif (user_input == "error"):
            if self.context.getNav():
                perCellError = self.form.solutionIncrement().energyErrorPerCell()
                soln = Funciton.solution(perCellError,self.form.solution())      
            else:
                perCellError = self.form.solution().energyErrorPerCell()
                soln = Function.solution(perCellError,self.form.solution())
	else:
            self.context.parse_error(user_input)
            plot([])
		#some sort of error message and reasking of input
	mesh = self.form.solution().mesh()
	refCellVertexPoints = [[-1.,-1.],[-1.,-.5],[-1.,.5],[-1.,1.],[-.5,-1.],[-.5,-.5],[-.5,.5],[-.5,1.],[.5,-1.],[.5,-.5],[.5,.5],[.5,1.][1.,-1.],[1.-.5],[1.,.5],[1.,1.]]
	activeCellIDs = mesh.getActiveCellIDs()
        print(activeCellIDs)
	values = []
	points = []
	for cellID in activeCellIDs:	
            (newValues,newPoints) = soln.getCellValues(mesh, cellID, refCellVertexPoints)
	    values.append(newValues)
	    points.append(newPoints) 
        plotter = Plotter(values, points, mesh)
        plotter

        #self.main()
        #no need to call itself. Context loops on this state until termination

    #refines the solution
    def refine(self, phrase):
	if (len(phrase) > 0):
	    words = phrase
	else:
            user_input = self.context.take_user_input("Would you like to refine geometrically (h) or using polynomialorder (p)?")
	    words = user_input.split()
	#hRefinement
	if (words[0] == 'h'):
	    if (words[-1:] == ["auto"]):
		self.form.hRefine()
                self.solve_equation()
	    elif (len (words) > 1):
                data = words[1:]
                cells_refine = []
                try:
                    cells_refine = self.parse_cells(data)
                except ValueError:
                    print("Error entering cells to refine\n")
                    print("Returning to refinement options")
                    self.refine([])
                    return
		self.form.solution().mesh().hRefine(cells_refine)
                self.solve_equation()
                return
	    else:
		user_input = self.context.take_user_input("Which elements? You can specify active element numbers (0,1,2,5,8,9,10,...) or auto.")
                if (user_input == "auto"):
                    self.form.hRefine()
                    self.solve_equation()
                else:
                    data = user_input.split(',')
                    try:
                        cells_refine = self.parse_cells(data)
                    except ValueError:
                        print("Error entering cells to refine\n")
                        print("Returning to refinement options")
                        self.refine([])
                        return
                    self.form.solution().mesh().hRefine(cells_refine)
                    self.solve_equation()
                    return
	#pRefinement
	elif (words[0] == 'p'):
            if (words[-1:] == ["auto"]):
                self.form.pRefine()
                self.solve_equation()
	    elif (len(words) > 1):
                data = words[1:]
                try:
                    cells_refine = self.parse_cells(data)
                except ValueError:
                    print("Error entering cells to refine\n")
                    print("Returning to refinement options")
                    self.refine([])
                    return
		self.form.solution().mesh().pRefine(cells_refine)
                self.solve_equation()
                return
	    else:
		user_input = self.context.take_user_input("Which elements? You can specify active element numbers (0,1,2,5,8,9,10,...) or auto.")
                if (user_input == "auto"):
                    self.form.pRefine()
                    self.solve_equation()
                else:
                    data = user_input.split(',')
                    try:
                        cells_refine = self.parse_cells(data)
                    except ValueError:
                        print("Error entering cells to refine\n")
                        print("Returning to refinement options")
                        self.refine([])
                        return
                    self.form.solution().mesh().pRefine(cells_refine)
                    self.solve_equation()
                    return
	#Input Error
	else:
	    self.context.parse_error(' '.join(words))
	    self.refine([])
            return

    #takes a list of str or int and returns a list of int
    def parse_cells(self, data):
        cells_refine = []
        for num in data:
            if (type(num) is str):
                new_stuff = (num.split(','))
                for val in new_stuff:
                    if(type(val) is str):
                        try:
                            cells_refine.append(int(val))
                        except ValueError:
                            raise ValueError("Could not convert to an int")
            elif (type(num) == int):
                        cells_refine.append(num)
        return cells_refine
    
    def solve_equation(self):
        if (self.context.getNav()):
            nonlinearThreshold = 1e-3
            normOfIncrement = 1
            stepNumber = 0
            while (normOfIncrement > nonlinearThreshold and stepNumber < 10):
                self.form.solveAndAccumulate()
                normOfIncrement = self.form.L2NormSolutionIncrement()
                print("L^2 norm of increment: %0.3f" % normOfIncrement)
                stepNumber += 1
            mesh = self.form.solution().mesh();
            energy = self.form.solutionIncrement().energyErrorTotal()
            self.context.incRef()
            self.context.printRefine(energy, mesh)
        else:
            self.form.solve()
            mesh = self.form.solution().mesh()
            energy = self.form.solution().energyErrorTotal()
            self.context.incRef()
            self.context.printRefine(energy, mesh)

    def display_error(self):
        if self.context.getNav():
            perCellError = self.form.solutionIncrement().energyErrorPerCell()
            for cellID in perCellError:
                if perCellError[cellID] > .01:
                    print("Energy error for cell %i: %0.3f" % (cellID, perCellError[cellID]))
        else:
            perCellError = self.form.solution().energyErrorPerCell()
            for cellID in perCellError:
                if perCellError[cellID] > .01:
                    print("Energy error for cell %i: %0.3f" % (cellID, perCellError[cellID]))

    #saves the solution
    def save(self, phrase):
	if (len(phrase) > 0):
	    user_input = phrase
	else:
	    user_input = self.context.take_user_input("What would you like to call the solution and Mesh files\n(may cancel with \'cancel\')\n")
	if (user_input.lower() == "cancel"):
	    print("Cancelled\n")
	    return
	elif (len(user_input) > 0):
	    print("Saving...\n")

            #Save in Camellia
            self.form.save(user_input)
            
            #writing to file what cannot be saved through Camillia
            f = open(user_input + ".txt", "w")
            f.write(self.context.saveString)
            f.close()
            f = open(user_input + "_refNum.txt", "w")
            f.write(str(self.context.getRef()))
            f.close()
            print("saved")
	    return
    
	else:
	    print("No name entered, returning to menu\n")
	    return

    def load(self, phrase):
	if (len(phrase) > 0):
	    user_input = phrase.split[1]
	else:
	    user_input = self.context.take_user_input("What file would you like to load? (type \"cancel\" to cancel loading)\n")
            if (user_input.lower() == "cancel"):
                print("Cancelled the load\n")
                return
	if self.context.file_exists(user_input):
            self.context.upload_file(user_input)
            self.context.switch_state(Creation.Creation(self.context))
            return
	print("That file does not exist in this folder\n")
	self.load(phrase)




