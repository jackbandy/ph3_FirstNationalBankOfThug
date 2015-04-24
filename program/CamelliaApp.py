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
        self.interpreter = Interpreter2.Interpreter2()

        self.funcs = [self.ids.func_1, self.ids.func_2, self.ids.func_3, self.ids.func_4, self.ids.func_5, self.ids.func_6, self.ids.func_7, self.ids.func_8]
        self.funcs_b = [self.ids.func_1b, self.ids.func_2b, self.ids.func_3b, self.ids.func_4b, self.ids.func_5b, self.ids.func_6b, self.ids.func_7b, self.ids.func_8b]
        self.poses = [self.ids.pos_1, self.ids.pos_2, self.ids.pos_3, self.ids.pos_4, self.ids.pos_5, self.ids.pos_6, self.ids.pos_7, self.ids.pos_8]
        self.flows = [self.ids.flow_1, self.ids.flow_2, self.ids.flow_3, self.ids.flow_4, self.ids.flow_5, self.ids.flow_6, self.ids.flow_7, self.ids.flow_8]
        self.inputs = self.funcs+self.funcs_b+self.poses+[self.ids.mesh_1, self.ids.mesh_2, self.ids.dim_1, self.ids.dim_2, self.ids.reyn, self.ids.load_file, self.ids.save_file]
        
        self.ids.state.disabled = True 
        self.ids.m_refine.disabled = True       

        for flow in self.flows:
            flow.bind(text=self.change_flow_input)
	    (self.ids.refine_type).bind(text=self.change_refine_input)
	

        self.ids.eq.bind(text=self.equation_choice)

    def solve(self):
        solveable = True
        inflow = []
        outflow = []
        for y in self.inputs:
            y.background_color = (1,1,1,1)
        reg = re.compile("[x,y][=,>,<][-+]?\d*\.?\d+")
        #checks if the functions and position are parsable, not useful
        for counter, flow  in enumerate(self.flows):
            if (flow.text == 'Inflow'):
                text = self.funcs[counter].text
                if (len(text) == 0):
                     text = '0'
                if (not self.checkFunction(text)):
                    solveable = False
                    self.color_red(self.funcs[counter])
                else:
                    fun_x = text
                text = self.funcs_b[counter].text
                if (len(text) == 0):
                     text = '0'
                if (not self.checkFunction(text)):
                    solveable = False
                    self.color_red(self.funcs_b[counter])
                else:
                    fun_y = text 
                text = self.poses[counter].text
                text = text.replace(" ","")
                filters = reg.findall(text)
                if (len(filters) == 0):
                    self.color_red(self.poses[counter])
                    solveable = False
                else:
                    pos = text
                if solveable:
                    inflow.append((pos, fun_x,fun_y))
            elif (flow.text == 'Outflow'):
                text = self.poses[counter].text
                text = text.replace(" ","")
                filters = reg.findall(text)
                if (len(filters) == 0):
                    self.color_red(self.poses[counter])
                    solveable = False
                else:
                    outflow.append(text)
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
            if (self.ids.eq.text == 'Navier-Stokes'):
                reyn = int(self.ids.reyn.text)
                if (reyn < 0):
                    self.color_red(self.ids.reyn)
                    solveable = False
        except ValueError:
            self.color_red(self.ids.reyn)
            solveable = False
        if (solveable):
            #solve
            #plot
            print(inflow)
            print(outflow)
            self.switch_tab()
            eq = self.ids.eq.text
            poly = self.ids.poly.text
            state = self.ids.state.text
            dim_1 = self.ids.dim_1.text
            dim_2 = self.ids.dim_2.text
            mesh_1 = self.ids.mesh_1.text
            mesh_2 = self.ids.mesh_2.text
            if self.ids.state.text == 'Stokes':
                reyn = "-1"
            else:
                reyn = self.ids.reyn.text
            self.control.solve(eq, poly, state, dim_1, dim_2, mesh_1, mesh_2, reyn, inflow, outflow)


    def checkFunction(self, text):
        try:
            func = self.interpreter.interpret(text)
        except NameError:
            return False
        return True

    def refine(self):
        text=self.ids.refine_type.text
        if text=="h auto" or text=="p auto":
            #self.control.autoRefine(text[0])
            self.ids.m_refine.background_color = (1,1,1,1)
        elif text=="p manual" or text=="h manual":
            elements = self.ids.m_refine.text
            elements = elements.replace(" ","")
            reg = re.compile("\d+(,\d+)*")
            m = reg.match(elements)
            if (m != None and elements==m.group() and elements!=""):
                self.ids.m_refine.background_color = (1,1,1,1)
                #self.control.manualRefine(text[0],elements)
            else:
                self.color_red(self.ids.m_refine)


    #go to the solution tab 
    def switch_tab(self):
	a = self.tab_list[0]
	self.switch_to(a)

    def change_refine_input(self, spinner, text):
        if text=="h auto" or text=="p auto":
            self.ids.m_refine.disabled = True
            self.ids.m_refine.background_color = (1,1,1,1)
        else:
            self.ids.m_refine.disabled = False
            

    #changes what can be input for the specified flow condition
    def change_flow_input(self, spinner, text):
        if (text == "Inflow"):
            for i in range(0, len(self.flows)):
                if spinner == self.flows[i]:
                    self.funcs[i].disabled = False
                    self.funcs_b[i].disabled = False
                    self.poses[i].disabled = False
                    break
        elif (text == "Outflow"):
            for i in range(0, len(self.flows)):
                if spinner == self.flows[i]:
                    self.funcs[i].disabled = True
                    self.funcs_b[i].disabled = True
                    self.poses[i].disabled = False
                    break
        elif (text == "N/A"):
            for i in range(0, len(self.flows)):
                if spinner == self.flows[i]:
                    self.funcs[i].disabled = True
                    self.funcs_b[i].disabled = True
                    self.poses[i].disabled = True
                    break

    def equation_choice(self,spinner, text):
        if (text == "Navier-Stokes"):
            self.ids.reyn.disabled = False
            self.ids.state.text = "Steady State"
            self.ids.state.disabled = True
        else:
            self.ids.reyn.disabled = True
            self.ids.reyn.background_color = (1, 1, 1, 1)
            self.ids.state.disabled = False

    def color_red(self, i):
        i.background_color = (.5, 0, 0.1, 1)

    def clear(self):
        self.ids.eq.text = 'Navier-Stokes'
        self.ids.poly.text = '1'
        self.ids.state.text = 'Steady State'
        self.ids.dim_1.text = ''
        self.ids.dim_2.text = ''
        self.ids.mesh_1.text = ''
        self.ids.mesh_2.text = ''
        self.ids.reyn.text = ''
        for widget in self.inputs:
            widget.disabled = False
            widget.text = ''
            widget.background_color = (1,1,1,1)
        for x in self.flows:
            x.text = 'Select In/Outflow'

    def save(self):
        text = self.ids.save_file.text
        if (len(text) > 0):
            self.control.save(text)
        else:
            self.control.save("CamelliaSaveFile")

    def load(self):
        text = self.ids.load_file.text
        if (len(text) == 0):
            pass
            #error
        else:
            boo = self.control.load(text)
            if (boo):
                self.plot()
                self.ids.error.text = self.control.error()
            else:
                pass
                #make red

    def plot(self):
        plot = self.ids.plot_type.text
        self.control.plot(plot)

class CamelliaApp(App):
    def build(self):
        return CamelliaWindow()



if __name__ == '__main__':
    CamelliaApp().run()
