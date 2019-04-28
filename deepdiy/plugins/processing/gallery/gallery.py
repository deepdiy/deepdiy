import sys,os
sys.path.append('../')
from utils.get_parent_path import get_parent_path

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import DictProperty
from kivy.uix.boxlayout import BoxLayout

class Gallery(BoxLayout):
	"""docstring for Gallery."""

	data=DictProperty()
	def __init__(self):
		super(Gallery, self).__init__()
