class Person:
    def __init__(self, name):
        self.name = name
        self.beyonce = None
    @staticmethod
    def getting_merried(husban, wife):
        husban.beyonce = wife
        wife.beyonce = husban
dave = Person(name="Dave")
joan = Person("Joan")
Person.getting_merried(dave, joan)
print(dave.beyonce.name)

