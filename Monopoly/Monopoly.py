class Board:
    def __init__(self):
        self.board = []

        # Create Board
        f = open('USBoard.txt')
        for line in f:
            self.board.append(str(line)[:-1])

    def __str__(self):
        return str(self.board)


class Player:
    def __init__(self, name, icon):
        self.playerName = name
        self.playerIcon = icon
        self.wallet = 1500
        self.properties = []

    def __str__(self):
        return self.playerName + ", " + self.playerIcon + ", " + str(self.wallet) + ", " + str(self.properties)

    def getWallet(self):
        return self.wallet

    def receiveMoney(self, amount):
        self.wallet += amount
        return

    def payMoney(self, amount):
        if self.wallet - amount < 0:return False
        self.wallet -= amount
        return True

    def calculateTotalPropertyValue(self):
        # NEED TO DO IT
        return 1

    def getProperty(self, prop):
        self.properties.append(prop)

    def giveProperty(self, prop):
        if not prop in self.properties:
            return False
        return self.properties.remove(prop)
        
class Property:
    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

class ColorProperty:
    def __init__(self, price, mortgageAmount, rentTuple):
        self.propertyPrice = price
        self.mortgageMount = mortgageAmount
        self.rentTuple = rentTuple

    
class TaxProperty(Property):
    def __init__(self, name, taxAmount, variableTax = False, variableRate = None):
        self.taxAmount = taxAmount
        self.variableTax = variableTax
        self.variableRate = variableRate
        super().__init__(name)

    def landAction(self, player):
        return self.__payTax(player)

    def __payTax(self, player):
        if self.variableTax:
            if self.variableRate * player.calculateTotalPropertyValue() < self.taxAmount:
                return player.payMoney(int(self.variableRate * player.calculateTotalPropertyValue()))
            else:
                return player.payMoney(self.taxAmount)
        else:
            return player.payMoney(self.taxAmount)
    
    
        
        
chris = Player("Chris", "boat")
chris.receiveMoney(1200)
print(chris)
chris.payMoney(23)
print(chris)

incomeTax = TaxProperty("Income", 200, True, .25)

print(incomeTax.getName())
incomeTax.landAction(chris)
print(chris)
