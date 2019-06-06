import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH
from middleware.widget_handler import WidgetHandler
from middleware.plugin_handler import PluginHandler
from kivy.app import App
from kivy.clock import Clock

def run():
	widget_handler=WidgetHandler()
	plugin_handler=PluginHandler()
	widget_handler.switch_screens('processing','rotation')
	bundle_dir=rootpath.detect(pattern='main.py')
	plugin_handler.set_plugin_attr(
		'files','path','D:\onedrive\program/for_liuyuan_rotation\data/test.tiff')
	# plugin_handler.data.select_idx = [0,0]

run()
