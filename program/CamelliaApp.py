from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.uix import *
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel
import Controller
import Interpreter2
from PyCamellia import *
import re




class CamelliaWindow(TabbedPanel):

    def __init__(self, **kwargs):
        super(CamelliaWindow, self).__init__(**kwargs)
        #filterit = lambda string: list(filter(lambda pair: pair[0].startswith(string), self.ids.iteritems()))
        #extract = lambda pairs: map(lambda pair: pair[1], pairs)
        #self.poses = extract(filterit('pos_'))
        #self.flows = extract(filterit('flow_'))
        #funcs = filterit('func_')
        #self.funcs_b = extract(filter(lambda pair: pair[0].endswith('b'), funcs))
        #self.funcs = extract(filter(lambda pair: not pair[0].endswith('b'), funcs))
        self.control = Controller.Controller()
        self.finterpreter = Interpreter2.Interpreter2()

        self.funcs = [self.ids.func_1, self.ids.func_2, self.ids.func_3, self.ids.func_4, self.ids.func_5, self.ids.func_6, self.ids.func_7, self.ids.func_8]
        self.funcs_b = [self.ids.func_1b, self.ids.func_2b, self.ids.func_3b, self.ids.func_4b, self.ids.func_5b, self.ids.func_6b, self.ids.func_7b, self.ids.func_8b]
        self.poses = [self.ids.pos_1, self.ids.pos_2, self.ids.pos_3, self.ids.pos_4, self.ids.pos_5, self.ids.pos_6, self.ids.pos_7, self.ids.pos_8]
        self.flows = [self.ids.flow_1, self.ids.flow_2, self.ids.flow_3, self.ids.flow_4, self.ids.flow_5, self.ids.flow_6, self.ids.flow_7, self.ids.flow_8]
        self.inputs = self.funcs+self.funcs_b+self.poses+[self.ids.mesh_1, self.ids.mesh_2, self.ids.dim_1, self.ids.dim_2, self.ids.reyn]
        
        #for flow in self.flows:
        #    flow.bind(text=self.change_input)

    def solve(self):
        solveable = True
        fun_x = []
        fun_y = []
        pos = []
        for y in self.inputs:
            y.background_color = (1,1,1,1)
        for counter, flow  in enumerate(self.flows):
            if (flow.text == 'Inflow'):
                text = self.funcs[counter].text
                if (len(text) == 0):
                     text = '0'
                if (not self.checkFunction(text)):
                    solveable = False
                    self.color_red(self.funcs[counter])
                else:
                    fun_x.append(text)
                text = self.funcs_b[counter].text
                if (len(text) == 0):
                     text = '0'
                if (not self.checkFunction(text)):
                    solveable = False
                    self.color_red(self.funcs_b[counter])
                else:
                    fun_y.append(text)
                #check positions
            elif (flow.text == 'Outflow'):
                #check pos
                pass
        #check dim and mesh as float and int respectively
        try:
            d_1 = float(self.ids.dim_1.text)
        except ValueError:
            self.color_red(self.ids.dim_1)
            solveable = False
        try:
            d_2 = float(self.ids.dim_2.text)
        except ValueError:
            self.color_red(self.ids.dim_2)
            solveable = False
        try:
            m_1 = int(self.ids.mesh_1.text)
        except ValueError:
            self.color_red(self.ids.mesh_1)
            solveable = False
        try:
            m_2 = int(self.ids.mesh_2.text)
        except ValueError:
            self.color_red(self.ids.mesh_2)
            solveable = False
        try:
            reyn = int(self.ids.reyn.text)
        except ValueError:
            self.color_red(self.ids.reyn)
            solveable = False
        print(solveable)
	if (solveable):
		self.switch_tab()
        #if stokes reyn = -1 else check it
        # pass the stuff
        #if (solveable):
            
            #string eq
            #string poly
            #string tuple mesh elements
            #string tuple dimensions
            
            #string reyn
            #reyn = self.ids.reyn.text positions
            #List<string> inflow positions
            #List<string> inflow x functions fun_x
            #List<string> inflow y functions fun_y
            #List<string> outflow positions


    #go to the solution tab 
    def switch_tab(self):
	a = self.tab_list[0]
	self.switch_to(a)

    def change_input(spinner, text):
        if (text == "Inflow"):
            self.funcs[0].disabled = False
            self.funcs_b[0].disabled = False
            self.poses[0].disabled = False
        elif (text == "Outflow"):
            self.funcs[0].disabled = True
            self.funcs_b[0].disabled = True
            self.poses[0].disabled = False
        elif (text == "N/A"):
            self.funcs[0].disabled = True
            self.funcs_b[0].disabled = True
            self.poses[0].disabled = True

    def color_red(self, i):
        i.background_color = (.5, 0, 0.1, 1)

    def clear(self):
        self.ids.eq.text = 'Navier-Stokes'
        self.ids.poly.text = '1'
        self.ids.state.text = 'Transient'
        self.ids.dim_1.text = ''
        self.ids.dim_2.text = ''
        self.ids.mesh_1.text = ''
        self.ids.mesh_2.text = ''
        self.ids.reyn.text = ''
        for x in self.poses:
            x.text = ''
        for x in self.flows:
            x.text = 'Select In/Outflow'
        for x in self.funcs:
            x.text = ''
        for x in self.funcs_b:
            x.text = ''
        for t_in in self.inputs:
            t_in.background_color = (1,1,1,1)

    def checkFunction(self, text):
        try:
            func = self.interpreter.interpret(text)
        except NameError:
            return False
        return True

    def save(self):
        name = self.ids.save_file.text
        self.controller.save(name)
    
    def load(self):
        name = self.ids.load_file.text
        data = self.controller.load(name)
        #do stuff with the data

class CamelliaApp(App):
    def build(self):
        return CamelliaWindow()



if __name__ == '__main__':
    CamelliaApp().run()
