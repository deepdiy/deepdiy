import sys,os
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
sys.path.append('../')

from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty,DictProperty,StringProperty,ListProperty


class Options(object):
    """docstring for Options."""

    def __init__(self, *arg):
        super(Options, self).__init__()




class Test(object):
    def __init__(self):
        super(Test, self).__init__()
        options=Options()

if __name__ == '__main__':
    test=Test()
