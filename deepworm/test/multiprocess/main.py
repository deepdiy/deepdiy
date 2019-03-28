from kivy.app import App
from kivy.properties import ObjectProperty,ListProperty,DictProperty,StringProperty,NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import multiprocessing

class Sub(App):

    data=NumericProperty(0)

    def __init__(self,**kwargs):
        super(Sub, self).__init__(**kwargs)
        self.window2=BoxLayout()
        self.window2.add_widget(Button(id='btn_foo',text='foo'))
        self.window2.ids = {child.id:child for child in self.window2.children}
        self.window2.ids.btn_foo.bind(on_release=self.update)

    def update(self,*args):
        self.data+=1
        self.window2.ids.btn_foo.text=str(self.data)

    def build(self):
        return self.window2

class MainWindow(App):
    data=NumericProperty()


    def __init__(self,**kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.window2=BoxLayout()
        self.window2.add_widget(Button(id='btn_foo',text='bar'))
        self.window2.ids = {child.id:child for child in self.window2.children}
        self.window2.ids.btn_foo.bind(on_release=self.update)

        # multiprocessing.Process(target=self.open_sub).start()

    def open_sub(self):
        self.sub=Sub()
        self.sub.run()

    def update(self,*args):
        self.data+=1
        self.window2.ids.btn_foo.text=str(self.data)

    def build(self):
        return self.window2

if __name__ == '__main__':
    MainWindow().run()
