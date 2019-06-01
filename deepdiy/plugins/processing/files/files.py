import os,rootpath
rootpath.append(pattern='main.py') # add the directory of main.py to PATH
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty,StringProperty
from utils.select_path_dialog import select_file,select_folder
from utils.get_file_list import get_file_list


class Files(BoxLayout):
	data=ObjectProperty()
	path=StringProperty()

	bundle_dir = rootpath.detect(pattern='main.py') # Obtain the dir of main.py
	Builder.load_file(bundle_dir +os.sep+'ui'+os.sep+'files.kv')

	def __init__(self):
		super(Files, self).__init__()
		self.bind(path=self.add_to_tree)

	def open_file(self):
		self.path=select_file()

	def open_folder(self):
		self.path=select_folder()

	def add_to_tree(self,*args):
		if self.path=='':
			return
		file_list={}
		file_list['image']=get_file_list(self.path,formats=['jpg','jpeg','bmp','png','tiff','tif'])
		file_list['video']=get_file_list(self.path,formats=['avi','mp4'])
		tree={'node_id':'resources','children':[],'type':'root'}
		for data_format in file_list:
			for file_path in file_list[data_format]:
				tree['children'].append({
					'node_id':file_path.split(os.sep)[-1],
					'type':'file_path',
					'content':file_path,
					'display':data_format+'_viewer',
					'children':[]})
		self.data.tree=tree
		self.property('data').dispatch(self)
		print(self.path)


class Test(App):
	def build(self):

		demo=Files()
		demo.data=lambda:None
		demo.data.tree={}
		return demo

if __name__ == '__main__':
	Test().run()
