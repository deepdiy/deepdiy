import sys,os
sys.path.append('../')
from utils.get_parent_path import get_parent_path

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty,DictProperty
from pysnooper import snoop

class Data(BoxLayout):
	"""docstring for Data."""

	file_list=ListProperty()
	select_idx=ListProperty()
	# tree=DictProperty()
	selected_data=DictProperty()

	bundle_dir = get_parent_path(3)

	def __init__(self):
		super(Data, self).__init__()

	# @snoop()
	def get_selected_data(self):
		self.selected_data=self.tree
		for i in self.select_idx[1:]:
			self.selected_data=self.selected_data['children'][i]
		if self.select_idx==[0]:
			self.selected_data=self.tree
		return self.selected_data

	def load_sample_data(self):
		self.select_idx=[0,0]
		self.tree={
			'node_id':'root',
			'type':None,
			'content':'',
			'display':None,
			'children':[{
				'node_id':'face.jpg',
				'type':'file_path',
				'content':os.sep.join([self.bundle_dir,'img','face.jpg']),
				'display':None,
				'children':[]
			}]}


class Test(App):
	def __init__(self,**kwargs):
		super(Test, self).__init__(**kwargs)

	def build(self):
		data=Data()
		data.load_sample_data()
		print(data.get_selected_data())
		return data

if __name__ == '__main__':
	Test().run()
