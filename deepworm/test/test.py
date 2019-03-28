import threading
import time
from kivy.app import App
from kivy.lang import Builder
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty

Builder.load_string('''
<Thread>:
    Button:
        text: "use thread"
        on_release: root.First_thread()
    Button:
        text: "Hit me"
        on_release: root.Counter_function()
    Label:
        id: lbl
        text: "Numbers"''')

class Thread(BoxLayout):
    counter = NumericProperty(0)

    def Counter_function(self):
        self.counter += 1
        self.ids.lbl.text = "{}".format(self.counter)

    def First_thread(self):
        threading.Thread(target = self.Counter_function).start()
        self.counter += 1
        self.ids.lbl.text = "{}".format(self.counter)

class MyApp(App):
    def build(self):
        self.load_kv('thread.kv')
        return Thread()

if __name__ == "__main__":
    app = MyApp()
    app.run()
