import sys,os
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
os.chdir(scriptPath)
sys.path.append('../')

from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty,DictProperty,StringProperty,ListProperty
from utils.get_file_list import get_file_list

class Resources(Widget):
    file_path=StringProperty()
    file_list=ListProperty()
    resource_data=DictProperty()
    resource_ids=DictProperty()
    selected_node=ObjectProperty()

    def __init__(self):
        super(Resources, self).__init__()
        self.bind(file_path=self.update_file_list)
        self.bind(file_list=self.update_ids)
        self.bind(resource_data=self.update_ids)

    def update_file_list(self,*arg):
        self.file_list=get_file_list(self.file_path)

    def update_ids(self,*arg):
        if self.file_list==[]:
            return
        resource_ids={}
        for file_path in self.file_list:
            resource_ids.update({file_path.split(os.sep)[-1]:[]})
        for dict in self.resource_data:
            if dict ==None:
                return
            for key in dict:
                resource_ids[key].append(dict[key])
        self.resource_ids={'All data':[resource_ids]}


class Test(object):
    def __init__(self):
        super(Test, self).__init__()
        resources=Resources()
        resources.file_path='D:\onedrive\program\worm_analyst/training\mask_rcnn\Mask_RCNN\dataset/train\img'
        print(resources.resource_ids)

if __name__ == '__main__':
    test=Test()
