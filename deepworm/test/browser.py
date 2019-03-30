#!/usr/bin/kivy
import kivy
kivy.require('1.7.2')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
import webbrowser

Builder.load_string('''
<MenuScreen>:
    GridLayout:
        padding: 5
        spacing: 5
        cols: 1
        padding: root.width*0.1
        Button:
            background_normal: ''
            background_color:(0.862, 0.078, 0.235, 0.9)
            text: 'PLAY'
            font_size: '20sp'
            on_press: root.val1()
''')

class MenuScreen(Screen):
    def val1(self):
        webbrowser.open("http://google.com/")

sm = ScreenManager()
menu = MenuScreen(name='menu')
sm.add_widget(menu)

class MainApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    MainApp().run()
