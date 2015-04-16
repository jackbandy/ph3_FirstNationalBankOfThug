from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.uix import *
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel
from time import sleep




class CamelliaWindow(TabbedPanel):
    def solve(self, i):
        i.text = 'Solving'
        i.disabled = True
    def clear(self, id):
        self.ids.eq.text = 'Navier-Stokes'
        self.ids.poly.text = '1'
        self.ids.state.text = 'Transient'
        self.ids.dim_1.text = ''
        self.ids.dim_2.text = ''
        self.ids.mesh_1.text = ''
        self.ids.mesh_2.text = ''
        self.ids.reyn.text = ''
        self.ids.pos_1.text = ''
        self.ids.pos_2.text = ''
        self.ids.pos_3.text = ''
        self.ids.pos_4.text = ''
        self.ids.pos_5.text = ''
        self.ids.pos_6.text = ''
        self.ids.pos_7.text = ''
        self.ids.pos_8.text = ''
        self.ids.flow_1.text = 'Select In/Outflow'
        self.ids.flow_2.text = 'Select In/Outflow'
        self.ids.flow_3.text = 'Select In/Outflow'
        self.ids.flow_4.text = 'Select In/Outflow'
        self.ids.flow_5.text = 'Select In/Outflow'
        self.ids.flow_6.text = 'Select In/Outflow'
        self.ids.flow_7.text = 'Select In/Outflow'
        self.ids.flow_8.text = 'Select In/Outflow'
        self.ids.func_1.text = ''
        self.ids.func_2.text = ''
        self.ids.func_3.text = ''
        self.ids.func_4.text = ''
        self.ids.func_5.text = ''
        self.ids.func_6.text = ''
        self.ids.func_7.text = ''
        self.ids.func_8.text = ''

class CamelliaApp(App):
    def build(self):
        return CamelliaWindow()



if __name__ == '__main__':
    CamelliaApp().run()
