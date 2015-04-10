#Left off: looking at widget.py, relativelayout.py, stacklayout.py. to_parent() in widget class, with relative=true. could be useful. But for now, keep working and then use that when we hit a road block.

from kivy.app import App
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget



class CamelliaApp(App):
    def build(self):
	parent = StackLayout(orientation = 'tb-lr')
	topLeft = StackLayout(orientation = 'tb-lr',size_hint=(.25,.5))
	totalHeightTopLeft = .9
	rowsTopLeft = 7
	heightTopLeft = totalHeightTopLeft/rowsTopLeft
	widthCol1 = 1


	topLeft.add_widget(Label(text='Equation', size_hint = (widthCol1,heightTopLeft)))
	topLeft.add_widget(TextInput(size_hint = (widthCol1, heightTopLeft)))
	topLeft.add_widget(Label(text='Poly Order:', size_hint = (widthCol1,heightTopLeft)))
	topLeft.add_widget(TextInput(size_hint = (widthCol1, heightTopLeft)))
	topLeft.add_widget(Label(text='Transient:', size_hint = (widthCol1,heightTopLeft)))
	topLeft.add_widget(TextInput(size_hint = (widthCol1, heightTopLeft)))
	topLeft.add_widget(Label(text='Dimensions:', size_hint = (widthCol1,heightTopLeft)))

	dimBoxes = StackLayout(orientation = 'lr-tb',size_hint=(.25,heightTopLeft*2))
	dimBoxes.add_widget(TextInput(size_hint = (widthCol1/2.0, heightTopLeft)))
	dimBoxes.add_widget(TextInput(size_hint = (widthCol1/2.0, heightTopLeft)))
	
	

	elemBoxes = StackLayout(orientation = 'lr-tb',size_hint=(.25,heightTopLeft*2))
	dimBoxes.add_widget(TextInput(size_hint = (widthCol1/2.0, heightTopLeft)))
	dimBoxes.add_widget(TextInput(size_hint = (widthCol1/2.0, heightTopLeft)))


	parent.add_widget(topLeft, 2)
	parent.add_widget(elemBoxes,0)
	
	parent.add_widget(dimBoxes, 1)
	
	
	
	#for i in range(25):
    	#	btn = Button(text=str(i), width=40 + i * 5, size_hint=(None, 0.15))
   	#	root.add_widget(btn)
        return parent


if __name__ == '__main__':
    CamelliaApp().run()
