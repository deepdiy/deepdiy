import sqlite3

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.popup import Popup


class TextInputPopup(Popup):
    obj = ObjectProperty(None)
    obj_text = StringProperty("")

    def __init__(self, obj, **kwargs):
        super(TextInputPopup, self).__init__(**kwargs)
        self.obj = obj
        self.obj_text = obj.text


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                  RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableButton(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

    def on_press(self):
        popup = TextInputPopup(self)
        popup.open()

    def update_changes(self, txt):
        self.text = txt


class RV(BoxLayout):
    data_items = ListProperty([])

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.get_users()

    def get_users(self):
        # connection = sqlite3.connect("demo.db")
        # cursor = connection.cursor()
        #
        # cursor.execute("SELECT * FROM Users ORDER BY UserID ASC")
        # rows = cursor.fetchall()
        #
        # # create data_items
        # for row in rows:
        #     for col in row:
        #         self.data_items.append(col)
        self.data_items=[1,2,3,4,5,6]


class TestApp(App):
    title = "Kivy RecycleView & SQLite3 Demo"

    def build(self):
        return RV()


if __name__ == "__main__":
    TestApp().run()
