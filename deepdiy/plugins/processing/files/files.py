import os,rootpath
rootpath.append(pattern='plugins')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty,StringProperty
from utils.select_path_dialog import select_file,select_folder
from utils.get_file_list import get_file_list


class Files(BoxLayout):
	data=ObjectProperty(BoxLayout())
	path=StringProperty()

	bundle_dir = rootpath.detect(pattern='plugins')
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'files.kv')

	def __init__(self):
		super(Files, self).__init__()
		self.bind(path=self.add_to_tree)
		self.data.apply_property(files_path=StringProperty('hi'))
		self.data.bind(files_path=self.setter('path'))

	def open_file(self):
		self.path=select_file()

	def open_folder(self):
		self.path=select_folder()

	def add_to_tree(self,*args):
		print(args)
		if self.path=='':
			return
		self.data.file_list=get_file_list(self.path,formats=['jpg','jpeg','bmp','png','tiff','tif'])
		tree={'node_id':'resources','children':[],'type':'root'}
		for file_path in self.data.file_list:
			tree['children'].append({
				'node_id':file_path.split(os.sep)[-1],
				'type':'file_path',
				'content':file_path,
				'display':'image_viewer',
				'children':[]})
		self.data.tree=tree
		self.property('data').dispatch(self)
		print(self.path)


class Test(App):
	def build(self):

		demo=Files()
		demo.data.files_path='d:/'
		return demo

if __name__ == '__main__':
	Test().run()
