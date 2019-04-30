from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty,DictProperty
from pysnooper import snoop

class Data(BoxLayout):
	"""docstring for Data."""

	select_idx=ListProperty()
	selected_data=DictProperty()
	def __init__(self):
		super(Data, self).__init__()

	# @snoop()
	def get_selected_data(self):
		self.selected_data=self.tree
		for i in self.select_idx[1:]:
			self.selected_data=self.selected_data['children'][i]
		if self.select_idx==[0]:
			self.selected_data=self.data.tree
		return self.selected_data


class Test(App):
	def __init__(self,**kwargs):
		super(Test, self).__init__(**kwargs)

	def build(self):
		data=Data()
		data.select_idx=[0,0]
		print(data.get_selected_data())
		return data

if __name__ == '__main__':
	Test().run()
