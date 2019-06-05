#!/usr/bin/python3
import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH
import logging
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty,DictProperty
from kivy.uix.boxlayout import BoxLayout

class WidgetHandler(BoxLayout):
	""" WidgetHandler help plugins to manipulate widgets in main window.

	Plugins call functions in this class to interact with main window,
	which ensures every plugin can be tested independetly without error.
	"""

	widget_manager=ObjectProperty()
	bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'widget_handler.kv')

	def __init__(self):
		super(WidgetHandler, self).__init__()
		self.bind(widget_manager=self._catch_screens)
		self._catch_main_window()

	def _catch_main_window(self):
		'''Catch the main window widget of running DeepDIY App'''
		app=App.get_running_app()
		if hasattr(app,'widget_manager'):
			self.widget_manager=app.widget_manager

	def _catch_screens(self,*args):
		'''Catch the screen manager in main window.

		There are two screen_manager in main window: processing_screens
		and display_screens. screen_managers are responsible for switching
		screens in processing panel and display panel. Screens are used to
		contain widgets from each plugin'''
		if self.widget_manager is not None:
			self.processing_screens=self.widget_manager.ids.processing_screens
			self.display_screens=self.widget_manager.ids.display_screens
			self.update_binding()

	def update_binding(self,*args):
		'''bind screen_names of screen_manager with spinner value
		bind spinner select event with switch_screens() function
		'''
		self.processing_screens.bind(screen_names=self.ids.spinner_processing_screens.setter('values'))
		self.ids.spinner_processing_screens.bind(text=lambda x,y:self.switch_screens('processing',y))
		self.display_screens.bind(screen_names=self.ids.spinner_display_screens.setter('values'))
		self.ids.spinner_display_screens.bind(text=lambda x,y:self.switch_screens('display',y))

	def switch_screens(self,pannel_id,screen_id):
		'''Switch screens by panel_id and screen_id
		Args:
			pannel_id: string, e.g. 'processing'
			screen_id: string, e.g. 'model_zoo'
		'''
		try:
			screen_mgr=getattr(self,pannel_id+'_screens')
			screen_mgr.current=screen_id
		except Exception as e:
			logging.warning(e)

	def set_progress_bar(self,value):
		try:
			self.widget_manager.ids.progress_bar.value=value
		except Exception as e:
			logging.warning(e)


class Test(App):
	"""docstring for Test."""

	def __init__(self):
		super(Test, self).__init__()

	def build(self):
		'''Testing by take this middleware as a plugin of main program'''
		from main import MainWindow
		from core.plugin_wrapper import PluginWrapper
		plugin_wrapper = PluginWrapper('plugins.processing.widget_handler')
		app = MainWindow()
		window = app.build()
		widget_handler=WidgetHandler()
		app.plugins['widget_handler']={
			'type':'processing','disabled':False,'wrapper':plugin_wrapper,'instance':widget_handler}
		return window

if __name__ == '__main__':
	Test().run()
