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
    def clear(self):
        self.ids.dim_2.disabled = False
        self.ids.dim_2.text = ''


class CamelliaApp(App):
    def build(self):
        return CamelliaWindow()



if __name__ == '__main__':
    CamelliaApp().run()
