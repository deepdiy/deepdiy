import sys,os
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
sys.path.append('../')

import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from utils.file_dialog import open_file,open_folder
from kivy.properties import StringProperty


class OpenPanel(BoxLayout):
    file_path=StringProperty('')
    folder_path=StringProperty('')
    def __init__(self):
        super(OpenPanel, self).__init__()
        # self.register_event_type('on_open_file')
        # self.register_event_type('on_open_folder')

    def open_file(self):
            self.file_path=open_file()
            print(self.file_path)
            # self.dispatch('on_open_file', 'test message')

    def open_folder(self):
        self.folder_path=open_folder()
        # self.dispatch('on_open_folder', 'test message')
        print(self.folder_path)

    def on_open_file(self, *args):
        pass

    def on_open_folder(self, *args):
        pass


class OpenPanelApp(App):
    def build(self):
        return OpenPanel()

if __name__ == '__main__':
    OpenPanelApp().run()
