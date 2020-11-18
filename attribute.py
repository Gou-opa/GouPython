class Fish:
    Type = "Animal"
    def __init__(self, kind):
        self.kind = kind

my_golden = Fish("Golden")
print(my_golden.Type)
print(my_golden.kind)
my_shark = Fish("Shark")
print(my_shark.Type)
print(my_shark.kind)

