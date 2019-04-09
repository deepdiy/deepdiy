from time import time
from kivy.properties import NumericProperty
from kivy.clock import Clock
from kivy.uix.widget import Widget

class Timer(Widget):

    time = NumericProperty(0)
    def __init__(self,**kwarg):
        super(Timer, self).__init__(**kwarg)
        Clock.schedule_interval(self._update_clock, 1 / 20.)

    def _update_clock(self, dt):
        self.time = time()
