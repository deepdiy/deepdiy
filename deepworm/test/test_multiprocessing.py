from multiprocessing import Process, Value, Lock
from multiprocessing.managers import BaseManager


class Employee(object):
    def __init__(self, name, salary):
        self.name = name
        self.salary = Value('i', salary)
        self.data=[]

    def increase(self):
        self.salary.value += 100
        self.data.append(self.salary.value)
        print(self.data)

    def getPay(self):
        return self.name + ':' + str(self.salary.value)


class MyManager(BaseManager):
    pass


def Manager2():
    m = MyManager()
    m.start()
    return m


MyManager.register('Employee', Employee)


def func1(em, lock):
    with lock:
        em.increase()


if __name__ == '__main__':
    manager = Manager2()
    em = manager.Employee('zhangsan', 1000)
    lock = Lock()
    proces = [Process(target=func1, args=(em, lock)) for i in range(10)]
    for p in proces:
        p.start()
    for p in proces:
        p.join()
    em.increase()
    print(em.getPay())
