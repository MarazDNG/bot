from datetime import datetime
import time


class C:
    def __init__(self) -> None:
        self.x = 5

    @property
    def time(self):
        return datetime.now()


def foo(t, f):
    print(t)
    print(f())
    time.sleep(1)
    print(t)
    print(f())


o = C()
foo(o.time, lambda: o.time)
