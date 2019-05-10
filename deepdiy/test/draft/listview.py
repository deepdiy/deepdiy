from kivy.app import App
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton, ListView,ListItemLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.listview import CompositeListItem


class Test(App):
	def build(self):
		args_converter = lambda row_index, rec: \
		    {'text': rec['text'],
		    'size_hint_y': None,
		    'height': 25,
		    'cls_dicts': [{'cls': ListItemButton,
		                    'kwargs': {'text': rec['text']}},
		                {'cls': ListItemLabel,
		                    'kwargs': {'text': "Middle-{0}".format(rec['text']),
		                            'is_representing_cls': True}},
		                {'cls': ListItemButton,
		                    'kwargs': {'text': rec['text']}}]}

		item_strings = ["{0}".format(index) for index in range(100)]

		integers_dict = \
		    {str(i): {'text': str(i), 'is_selected': False} for i in range(100)}

		dict_adapter = DictAdapter(sorted_keys=item_strings,
		                           data=integers_dict,
		                           args_converter=args_converter,
		                           selection_mode='single',
		                           allow_empty_selection=False,
		                           cls=CompositeListItem)

		list_view = ListView(adapter=dict_adapter)
		return list_view

Test().run()
