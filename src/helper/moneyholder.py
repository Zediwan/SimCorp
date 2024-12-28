class Moneyholder():
    def __init__(self):
        self.money: float = 0.0

    def gain_money(self, amount: float):
        self.money += amount
        
        #print(f"{self} gained {amount} money.")
    
    def spend_money(self, amount: float):
        if amount > self.money:
            raise NotEnoughMoneyException(f"{self} does not have enough money to spend ${amount}.")

        self.money -= amount
        
        #print(f"{self} spent {amount} money.")
        
class NotEnoughMoneyException(Exception):
    def __init__(self, message):
        super().__init__(message)