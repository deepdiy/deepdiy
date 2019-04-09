from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.label import Label

class FormParser(BoxLayout):
    """docstring for FormParser."""
    form=ListProperty()
    def __init__(self):
        super(FormParser, self).__init__()
        self.parse_tools={
            'spinner':self.add_spinner,
            'slider':self.add_slider,
            'path':self.add_path_selector}
        self.bind(form=self.parse)
        self.spin='a'

    def parse(self,*args):
        for i in self.form:
            self.parse_tools[i['type']](i)

    def alert(slef,*arg):
        print('hi')

    def add_spinner(self,config):
        spinner=Spinner(
            id=config['id'],
            text=config['text'],
            values=config['values'],
            size_hint_y=None,
            height='48dp')
        self.add_widget(spinner)
        self.add_binding(config['id'],config['target'])

    def add_slider(self,config):
        slider=Slider(
            id=config['id'],
            min=config['min'],
            max=config['max'],
            value=config['value'],
            size_hint_y=None,
            height='48dp')
        self.add_widget(slider)

    def add_binding(self,id,target):
        self.ids = {child.id:child for child in self.children}
        if not hasattr(self,target):
            self.__setattr__(target,None)
        self.ids[id].bind(text=lambda instance,value:self.__setattr__(target,value))

    def add_path_selector(self):
        pass


class Test(App):
    """docstring for Test."""

    def __init__(self):
        super(Test, self).__init__()

    def build(self):
        form_parser=FormParser()
        form_parser.form=[
            {
                'type':'spinner',
                'id':'spin1',
                'target':'spin',
                'text':'foo',
                'values':['a','b','c']
            },{
                'type':'slider',
                'id':'slider1',
                'target':'slid',
                'min':1,
                'max':100,
                'value':20
            }
        ]
        return form_parser


if __name__ == '__main__':
    test=Test().run()
