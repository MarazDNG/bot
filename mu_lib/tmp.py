
class C:
    def __init__(self) -> None:
        self.x = 5

o = C()
o.x = 1
print(o.x)
o.__init__()
print(o.x)
