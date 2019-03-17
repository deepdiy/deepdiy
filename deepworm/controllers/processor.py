
import sys,os
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
sys.path.append('../')

from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty


class Processor(Widget):
    resources=ObjectProperty(None, allownone=True)
    options=ObjectProperty(None, allownone=True)
    results=ObjectProperty(None, allownone=True)

    def __init__(self,**kwargs):
        super(ImageViewer, self).__init__(**kwargs)
        self.bind(options=self.run)

    def run(self):
        if options.is_running_maskrcnn==True:
            path=resources.selection
            result=mask_rcnn(path)
            updata_results()
            options.is_running_maskrcnn=False()
