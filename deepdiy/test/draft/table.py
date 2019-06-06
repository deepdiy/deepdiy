from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.properties import DictProperty, NumericProperty, StringProperty, \
                            BooleanProperty, ObjectProperty
from operator import itemgetter
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

Builder.load_string("""
<ColHeader>:
    bold: True
    on_press: self.data_table.sort_by(self.text)
<RowHeader>:
    background_down: self.background_normal
<EditableCell>:
    multiline: False
    on_focus: if not self.focus: self.data_table.data_update(self.id, self.text)
<StaticCell>:
    halign: 'left'
<DataTable>:
    id: table_grid
    cols: self.ncol
""")

class ColHeader(Button):
    #For some reason, adding this property as part of a
    #dynamic class declaration was failing.
    data_table = ObjectProperty(None)

class RowHeader(Button):
    data_table = ObjectProperty(None)
    initial_type = ObjectProperty(None)

class EditableCell(TextInput):
    data_table = ObjectProperty(None)
    initial_type = ObjectProperty(None)

class StaticCell(Label):
    data_table = ObjectProperty(None)
    initial_type = ObjectProperty(None)


class DataTable(GridLayout):
    """This is a compound widget designed to display
    a dictionary of data as a nice table. The dictionary
    should have the column headers as keys, and then
    the associated value is a list of data for that
    column.

    You may have lists of different lengths, but the columns
    will fill from the top down; therefore, include blank
    strings as placeholders for any empty cells.

    Note that since the column headers are dict keys, you
    must have unique column names. Sorry..."""
    data = DictProperty({})
    ncol = NumericProperty(0)
    nrow = NumericProperty(0)
    editable = BooleanProperty(False)
    header_col = StringProperty('')

    def __init__(self, data = {}, editable = False, header_column = '',
                 header_row = [], **kw):
        super(DataTable, self).__init__(**kw)
        self.data = data
        self.ncol = len(data)
        self.editable = editable
        self.header_col = header_column
        self.header_row = header_row
        celltype = EditableCell if self.editable else StaticCell
        self.nrow = max([len(data[x]) for x in data])
        self.cells = {}
        for key in self.header_row:
            cell_id = str(key)+'_head'
            cell = ColHeader(text = str(key), data_table = self, id = cell_id)
            self.cells[cell_id] = cell
            self.add_widget(cell)
        for i in range(self.nrow):
            get = itemgetter(i)
            for key in self.header_row:
                cell_id = str(key)+'_'+str(i)
                if i <= len(self.data[key]):
                    text = get(self.data[key])
                else:
                    text = ''
                    self.data[key].append('')
                if key == self.header_col:
                    self.cells[cell_id] = RowHeader(text = str(text), data_table = self,
                                                    id = cell_id, initial_type = type(text))
                else:
                    self.cells[cell_id] = celltype(text = str(text), data_table = self,
                                                   id = cell_id, initial_type = type(text))
                self.add_widget(self.cells[cell_id])

    def data_update(self, cell_id, value):
        """This will try to convert the value
        to the initial type of the data. If that fails,
        it'll just be a string. The initial type won't
        change, however."""
        key, idx = cell_id.split('_')
        try:
            val = self.cells[cell_id].initial_type(value)
        except ValueError:
            val = value
        self.data[key][int(idx)] = val

    def sort_by(self, colname):
        column_to_order = enumerate(self.data[colname])
        sort_order = map(itemgetter(0),
                         sorted(column_to_order, key=itemgetter(1)))
        for key in self.data:
            col = self.data[key]
            self.data[key] = [col[x] for x in sort_order]
            self.cells[str(key)+'_head'].background_color = (1, 1, 1, 1)
            for i in xrange(self.nrow):
                self.cells[str(key)+'_'+str(i)].text = str(self.data[key][i])
        self.cells[colname+'_head'].background_color = (0, 1, 0, 1)

if __name__ == '__main__':
    import random
    data = {'Col1':[random.random() for x in xrange(10)],
            'Col2':[random.random() for x in xrange(10)],
            'Col3':[random.random() for x in xrange(10)],
            'Col4':[random.random() for x in xrange(10)],
            'Col5':[random.random() for x in xrange(10)]}
    from kivy.base import runTouchApp
    from kivy.uix.pagelayout import PageLayout
    from kivy.factory import Factory
    Builder.load_string("""
<Page@AnchorLayout>:
    canvas.before:
        Color:
            rgba: 0, 0, 0, 1
        Rectangle:
            pos: self.pos
            size: self.size
    """)

    pg = PageLayout()
    staticpage = Factory.Page(name='static')
    staticpage.add_widget(DataTable(name = 'static', data=data, header_column = 'Col1',
                                    header_row = ['Col'+str(x+1) for x in xrange(5)]))
    editpage = Factory.Page(name='edit')
    editpage.add_widget(DataTable(name = 'edit', data=data, header_column = 'Col5',
                                  header_row = ['Col'+str(5-x) for x in xrange(5)],
                                  editable = True))
    pg.add_widget(staticpage)
    pg.add_widget(editpage)
    runTouchApp(pg)
