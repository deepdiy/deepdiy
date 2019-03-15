import sys,os
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
sys.path.append('../')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty,ObjectProperty,DictProperty
from controllers.image_viewer import ImageViewer
# from controllers.table_viewer import TableViewer
# from controllers.markdown_viewer import MarkdownViewer

class ResultPanel(BoxLayout):
    # data=DictProperty({'type':'blank'})
    data={'type':'blank'}
    page=StringProperty(data['type'])

    def __init__(self,**kwargs):
        super(ResultPanel, self).__init__(**kwargs)
        self.pages={
        'image':ImageViewer(),
        # 'table':TableViewer(),
        # 'markdown':MarkdownViewer(),
        'blank':BoxLayout()
        }
        self.bind(page=self.update_page)
        self.update_page()

    def update_page(self,*args):
        self.clear_widgets()
        self.add_widget(self.pages[self.page])
        self.ids = {child.id:child for child in self.children}

class TestApp(App):
    def build(self):
        return ResultPanel()

if __name__ == '__main__':
    TestApp().run()
