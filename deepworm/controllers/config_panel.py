import sys,os
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
sys.path.append('../')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from controllers.select_path_panel import SelectPathPanel
from controllers.detect_panel import DetectPanel
from controllers.segment_panel import SegmentPanel
from controllers.measure_panel import MeasurePanel
from controllers.train_panel import TrainPanel

class ConfigPanel(BoxLayout):
    page=StringProperty('Open')

    def __init__(self,**kwargs):
        super(ConfigPanel, self).__init__(**kwargs)
        self.pages={
        'Open':SelectPathPanel(),
        'Detect':DetectPanel(),
        'Segment':SegmentPanel(),
        'Measure':MeasurePanel(),
        'Train':TrainPanel()
        }
        self.bind(page=self.update_page)
        self.update_page()

    # frame.ids.options.
    def update_page(self,*args):
        self.clear_widgets()
        self.add_widget(self.pages[self.page])
        self.ids = {child.id:child for child in self.children}

class TestApp(App):
    def build(self):
        return ConfigPanel()

if __name__ == '__main__':
    TestApp().run()
