class InteractWithWallet:
    def interact(self, wallet):
        pass

class Fish(InteractWithWallet):
    def __init__(self):
        self.value = 100
        self.type = "Shark"
    def interact(self, wallet):
        wallet += self.value


class Bullet(InteractWithWallet):
    def __init__(self, bullet_type):
        self.type = bullet_type
        self.value = 10
    def interact(self, wallet):
        wallet -= self.value

class Player:
    def __init__(self):
        self.name = "HSGS"
        self.wallet = 1000
        self.arm = Bullet("spray")

