import multiprocessing
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget

class MainRoot(Widget):
    pass

class OtherRoot(Widget):
    pass

class MainApp(App):
    def build(self):
        Builder.load_file('B:\Python_Codes\Testing Grounds\shared.kv')
        main = MainRoot()
        return main

class OtherApp(App):
    def build(self):
        Builder.load_file('B:\Python_Codes\Testing Grounds\shared.kv')
        other = OtherRoot()
        return other

def open_parent():
    MainApp().run()

def open_child():
    OtherApp().run()

if __name__ == '__main__':
    a = multiprocessing.Process(target=open_parent)
    b = multiprocessing.Process(target=open_child)
    a.start()
    b.start()
