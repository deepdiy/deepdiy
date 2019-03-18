import sys,os
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
sys.path.append('../')

from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

class Frame(BoxLayout):
    Builder.load_file('../views/frame.kv')
