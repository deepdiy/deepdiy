from pebble import concurrent

def run_in_thread(fn):
    def run(*k, **kw):
        t = threading.Thread(target=fn, args=k, kwargs=kw)
        t.start()
        return t # <-- this is new!
    return run

@concurrent.thread
def plus(input):
    return input+1

print(plus(1).result())

print([0][1:])
