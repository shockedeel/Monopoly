class Board:
    def __init__(self):
        self.board = []

        # Create Board
        f = open('USBoard.txt')
        for line in f:
            # Strip newline and create property info tuple
            line = line[:-1]
            propertyInfo = tuple(line.split('-'))

            # Create Property based on info in property tuple
            if propertyInfo[1] == "color":
                rentInfo = tuple(map(int, propertyInfo[4].split(",")))
                self.board.append(ColorProperty(propertyInfo[0],int(propertyInfo[2]),int(propertyInfo[2]) / 2, rentInfo))

            if propertyInfo[1] == "go":
                self.board.append(GoProperty(propertyInfo[0]))

            if propertyInfo[1] == "tax":
                self.board.append(TaxProperty(propertyInfo[0], str(propertyInfo[4]),bool(propertyInfo[2]),float(propertyInfo[3])))

    def __str__(self):
        return str(self.board)


class Player:
    def __init__(self, name, icon = ''):
        self.playerName = name
        self.playerIcon = icon
        self.wallet = 1500
        self.properties = []

    def __repr__(self):
        return "(" + self.__str__() + ")"

    def __str__(self):
        return self.playerName + ", " + self.playerIcon + ", " + str(self.wallet) + ", " + str(self.properties)

    def getPlayerName(self):
        return self.playerName

    def getWallet(self):
        return self.wallet

    def receiveMoney(self, amount):
        self.wallet += amount
        return True

    def payMoney(self, amount):
        if self.wallet - amount < 0:return False
        self.wallet -= amount
        return True

    def calculateTotalPropertyValue(self):
        totalPropValue = 0
        for prop in self.properties:
            totalPropValue += prop.getPrice(self)
        return totalPropValue

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

    def __str__(self):
        return self.getName()

    def __repr__(self):
        return "(" + self.__str__() + ")"


class GoProperty(Property):
    def __init__(self, name):
        super().__init__(name)


class ColorProperty(Property):
    def __init__(self, name, price, mortgageAmount, rentTuple):
        self.propertyPrice = price
        self.owner = None
        self.mortgageAmount = mortgageAmount
        self.mortgageStatus = False
        self.rentTuple = rentTuple
        self.houseCount = 0
        super().__init__(name)

    def __str__(self):
        string = self.name + " " + str(self.propertyPrice) + " " +  str(self.owner) + " " +  str(self.mortgageStatus) + " " + str(self.houseCount)
        return string

    def getRentPrice(self):
        return self.rentTuple(self.houseCount)

    def getMortgageStatus(self):
        return self.mortgageStatus

    def getHouseCount(self):
        return self.houseCount

    def landAction(self, player):
        if self.owner == None:
            pass #TODO ask player if they want to buy
        elif self.owner != player.getPlayerName():
            return self.owner.receiveMoney(player.payMoney(self.getRentPrice()))

    def getPrice(self):
        return self.propertyPrice


class TaxProperty(Property):
    def __init__(self, name, taxAmount, variableTax = False, variableRate = None):
        self.taxAmount = taxAmount
        self.variableTax = variableTax
        self.variableRate = variableRate
        super().__init__(name)

    def __str__(self):
        return self.name + " " + str(self.taxAmount)

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

    class Deck:
        def __init__(self, type):
            self.type = type
            self.deck = []
            self.index = 0

        def fillDeck(self):
            if (self.type == 'CommunityChest'):
                f = open('CommunityChest.txt')
            if (self.type == 'Chance'):
                f = open('Chance.txt')
            for line in f:
                self.deck.append(str(line)[:-1])

        def printDeck(self):
            for element in self.deck:
                print(element)

        def shuffleDeck(self):
            shuffle(self.deck)

        def drawCard(self):
            if (self.index == len(self.deck)):
                self.index = 0
                self.shuffleDeck()
            index = self.index
            self.index += 1

            return self.deck[index]
    

class Monopoly():
    def __init__(self, playerInfo, boardType = "US"):
        self.players = []
        for x in range(len(playerInfo)):
            self.players.append(Player(playerInfo[x][0]))

        self.communityChest = 0

    def __str__(self):
        return str(self.players)



playerInfo = [("Chris", "Car"), ("Kolbe", "Boat")]
game = Monopoly(playerInfo)
print(game)

prop = ColorProperty("hello",200,100,(2,4,6,8,9,10))
board = Board()
print(board)
