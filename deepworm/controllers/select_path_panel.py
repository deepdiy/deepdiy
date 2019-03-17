import sys,os
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
sys.path.append('../')
from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.properties import StringProperty
from kivy.properties import DictProperty
from utils.select_path_dialog import select_file,select_folder

class SelectPathPanel(BoxLayout):
    file_path=StringProperty('')
    tree=DictProperty()
    id='select_path_panel'
    Builder.load_file('../views/select_path_panel.kv')

    def open_file(self):
        self.file_path=select_file()
        print(self.file_path)

    def open_folder(self):
        self.file_path=select_folder()
        print(self.file_path)


class Test(App):
    def build(self):
        return SelectPathPanel()

if __name__ == '__main__':
    Test().run()
