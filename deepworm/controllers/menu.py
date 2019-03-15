from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty


class Menu(BoxLayout):
    current_state=StringProperty('Open')

    def on_state(self, togglebutton):
        if togglebutton.state=='down':
            self.current_state=togglebutton.text
