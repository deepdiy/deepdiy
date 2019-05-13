import os,rootpath
rootpath.append(pattern='plugins')

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import DictProperty,StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window, Keyboard
from kivy.logger import Logger

class Hotkey(BoxLayout):
	"""docstring for Hotkey."""

	bundle_dir = rootpath.detect(pattern='plugins')
	# Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'gallery.kv')
	data=DictProperty()
	def __init__(self,**kwargs):
		super(Hotkey, self).__init__(**kwargs)
		self.super = []

		text = StringProperty()

		keyboard = Window.request_keyboard(self._keyboard_released, self)
		keyboard.bind(on_key_down=self._keyboard_on_key_down, on_key_up=self._keyboard_released)

		########################################
	#end def __init__

	def _keyboard_released(self, window, keycode):
		self.super = []

	def _keyboard_on_key_down(self, window, keycode, text, super):
		if 'lctrl' in self.super and keycode[1] == 's':
			app=App.get_running_app()
			app.plugin_manager.open()
			Logger.info("Item saved, {}".format(self.super))
			self.super = []
			return False
		elif 'lctrl' not in self.super and keycode[1] in ["lctrl"]:
			self.super.append(keycode[1])
			return False
		else:
			Logger.info("key {} pressed.".format(keycode))
			return False


class Test(App):
	"""docstring for Test."""

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		demo=Hotkey()
		return demo

if __name__ == '__main__':
	Test().run()
