from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.uix import *
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel




class CamelliaWindow(TabbedPanel):
    pass
        


class CamelliaApp(App):
    def build(self):
        return CamelliaWindow()



if __name__ == '__main__':
    CamelliaApp().run()
