"""This script demonstrates the overhead of using SyncManager vs Value.
Output:
    C double:        8.782e-07 sec per assignment
    C struct:        8.795e-07 sec per assignment
    Python class:    3.346e-07 sec per assignment
    AutoProxy:       2.985e-05 sec per assignment
Method calls on AutoProxy seem to be two orders of magnitude slower.
"""

import multiprocessing as mp
import multiprocessing.managers as mpm
import ctypes
import time


## number of iterations per type
n = 10000000


## Modifying a basic C type

val = mp.Value(ctypes.c_double)
t0 = time.time()
for i in range(n):
    val.value = i
ctype_time = (time.time() - t0)/n

print("C double:\t {:.4} sec per assignment".format(ctype_time))


## Modifying a C structure

class S(ctypes.Structure):
    _fields_ = [("value", ctypes.c_double)]
val = mp.Value(S)
t0 = time.time()
for i in range(n):
    val.value = i
cstruct_time = (time.time() - t0)/n

print("C struct:\t {:.4} sec per assignment".format(cstruct_time))


## Modifying a Python object via its setter method

class P:
    def __init__(self, value):
        self.value = value
    def set(self, value):
        self.value = value
    def get(self):
        return self.value
val = P(0.0)
t0 = time.time()
for i in range(n):
    val.set(i)
pysetter_time = (time.time() - t0)/n

print("Python class:\t {:.4} sec per assignment".format(pysetter_time))


## Modifying a Python object via SyncManager and AutoProxy

sm = mpm.SyncManager()
sm.register("pyval", P)
sm.start()
val = sm.pyval(0.0)
t0 = time.time()
for i in range(n):
    val.set(i)
autoproxy_time = (time.time() - t0)/n

print("AutoProxy:\t {:.4} sec per assignment".format(autoproxy_time))
