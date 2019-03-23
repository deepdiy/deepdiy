from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

class DetectPanel(BoxLayout):
    Builder.load_file('../views/detect_panel.kv')
    id='detect_panel'
