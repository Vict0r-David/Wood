#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from kivy.app import App
from kivy.config import Config 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty

#from kivy.uix.spinner import Spinner
class InfoForm(BoxLayout):
    r_input = ObjectProperty()
    e_input = ObjectProperty()
    p1_input = ObjectProperty()
    p2_input = ObjectProperty()
    aire_label = ObjectProperty()
        
    def _compute(self, source):
        aire = int(self.r_input.text) * int(self.r_input.text) * 3.14159 
        self.aire_label.text = 'L\'aire du tronc est de {} .'.format(aire)
    pass

class InfoApp(App):
    def build(self):
        self.title = 'VD Cutting Plans'
    pass
    
Config.set('graphics', 'width', '800') 
Config.set('graphics', 'height', '400')

InfoApp().run()
