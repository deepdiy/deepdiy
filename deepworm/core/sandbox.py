import threading
from kivy.event import EventDispatcher
from kivy.properties import ListProperty

class Sandbox(EventDispatcher):
    """docstring for ."""

    def __init__(self, func):
        super(Sandbox, self).__init__()
        self.input=ListProperty([])
        self.output=ListProperty([])
        self.log=ListProperty([])
        self.func = func

    def action(self):
        try:
            self.output=self.func(self.input[0])
        except Exception as e:
            self.log.append(e)

    def run(self):
        threading.Thread(target=self.action).start()


def worker(input):
    return input+1

def test():
    sandbox=Sandbox(worker)
    sandbox.input=[1]
    sandbox.run()
    print(sandbox.output)

if __name__ == '__main__':
    test()
