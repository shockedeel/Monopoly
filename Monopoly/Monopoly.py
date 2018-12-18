import random

class Board:
    def __init__(self):
        self.board = self.createBoard()

    def __iter__(self):
        return iter(self.board)

    def __getitem__(self, i):
        return self.board[i]

    def __str__(self):
        return str(self.board)

    def __len__(self):
        return len(self.board)

    def createBoard(self):
        board = []
        f = open('USBoard.txt')
        for line in f:
            # Strip newline and create property info tuple
            line = line[:-1]
            propertyInfo = tuple(line.split('-'))

            # Create Property based on info in property tuple
            if propertyInfo[1] == "color":
                rentInfo = tuple(map(int, propertyInfo[4].split(",")))
                board.append(
                    ColorProperty(propertyInfo[0], int(propertyInfo[2]), int(propertyInfo[2]) / 2, rentInfo))

            if propertyInfo[1] == "go":
                board.append(GoProperty(propertyInfo[0]))

            if propertyInfo[1] == "tax":
                board.append(
                    TaxProperty(propertyInfo[0], str(propertyInfo[4]), bool(propertyInfo[2]), float(propertyInfo[3])))

            if propertyInfo[1] == "rail":
                board.append(RailProperty(propertyInfo[0], int(propertyInfo[2]), int(propertyInfo[2]) / 2))

            if propertyInfo[1] == "chance":
                board.append(ChanceProperty(propertyInfo[0]))

            if propertyInfo[1] == "community chest":
                board.append(CommunityChestProperty(propertyInfo[0]))

            if propertyInfo[1] == "jail":
                board.append(JailProperty(propertyInfo[0]))

            if propertyInfo[1] == "goJail":
                board.append(GoJailProperty(propertyInfo[0]))

            if propertyInfo[1] == "parking":
                board.append(FreeParkingProperty(propertyInfo[0]))

            if propertyInfo[1] == "util":
                board.append(UtilityProperty(propertyInfo[0], propertyInfo[2]))

        return board

    def getPropertyName(self, index):
        return self.board[index].getName()


class Player:
    def __init__(self, name, icon = ''):
        self.playerName = name
        self.playerIcon = icon
        self.playerLocation = 0
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

    def movePlayer(self, roll, max):
        self.playerLocation += roll
        if self.playerLocation > max:
            self.playerLocation = self.playerLocation - max



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


class ChanceProperty(Property):
    def __init__(self, name):
        super().__init__(name)

    def landAction(self):

        pass


class CommunityChestProperty(Property):
    def __init__(self, name):
        super().__init__(name)

    def landAction(self):
        #TODO Fix
        pass


class JailProperty(Property):
    def __init__(self, name):
        super().__init__(name)

    def landAction(self):
        #TODO Fix
        pass


class GoJailProperty(Property):
    def __init__(self, name):
        super().__init__(name)

    def landAction(self):
        #TODO Fix
        pass


class FreeParkingProperty(Property):
    def __init__(self, name):
        super().__init__(name)
        self.potValue = 0

    def landAction(self):
        #TODO Fix
        pass

class UtilityProperty(Property):
    def __init__(self, name, price):
        super().__init__(name)
        self.price = price

    def __str__(self):
        return super().__str__() + " " + str(self.price)

    def landAction(self):
        #TODO Fix
        pass


class RailProperty(Property):
    def __init__(self, name, price, mortgageAmount):
        self.propertyPrice = price
        self.owner = None
        self.mortgageAmount = mortgageAmount
        self.mortgageStatus = False
        super().__init__(name)

    def __str__(self):
        string = self.name + " " + str(self.propertyPrice) + " " +  str(self.owner) + " " +  str(self.mortgageStatus)
        return string


    def getMortgageStatus(self):
        return self.mortgageStatus

    def getPrice(self):
        return self.propertyPrice


class ColorProperty(RailProperty):
    def __init__(self, name, price, mortgageAmount, rentTuple):
        self.rentTuple = rentTuple
        self.houseCount = 0
        super().__init__(name, price, mortgageAmount)

    def __str__(self):
        string = self.name + " " + str(self.propertyPrice) + " " + str(self.owner) + " " + str(
            self.mortgageStatus) + " " + str(self.houseCount)
        return string

    def getRentPrice(self):
        return self.rentTuple(self.houseCount)

    def getHouseCount(self):
        return self.houseCount

    def landAction(self, player):
        if self.owner == None:
            pass  # TODO ask player if they want to buy
        elif self.owner != player.getPlayerName():
            return self.owner.receiveMoney(player.payMoney(self.getRentPrice()))


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
    def __init__(self):
        self.deck = []
        self.index = 0

    def __str__(self):
        print(self.deck)

    def shuffleDeck(self):
        self.shuffle(self.deck)
        self.index = 0

    def drawCard(self):
        if self.index == len(self.deck) - 1:
            self.index = 0
        card = self.deck[self.index]
        self.index += 1
        return card


class CommunityChestDeck(Deck):
    def __init__(self):
        super().__init__()
        f = open("CommunityChest.txt")
        for line in f:
            self.deck.append(str(line)[:-1])


class ChanceDeck(Deck):
    def __init__(self):
        super().__init__()
        f = open("Chance.txt")
        for line in f:
            self.deck.append(str(line)[:-1])

class Dice():
    def __init__(self):
        self.doublesCount = 0

    def rollDice(self):
        dieOne = random.randint(1, 6)
        dieTwo = random.randint(1, 6)
        if dieOne == dieTwo:
            self.doublesCount += 1

        return dieOne, dieTwo

    def doublesCount(self):
        return self.doublesCount


class Monopoly():
    def __init__(self, playerInfo, boardType = "US"):
        self.players = []
        for x in range(len(playerInfo)):
            self.players.append(Player(playerInfo[x][0], playerInfo[x][1]))

        self.board = Board()
        self.communityChest = CommunityChestDeck()
        self.chance = ChanceDeck()

    def __str__(self):
        string = ""
        for player in self.players:
            string += "(" + str(player) + ", " + str(self.board.getPropertyName(player.playerLocation)) + ") "
        return string

    def playerTurn(self, player):
        dice = Dice()
        move = sum(dice.rollDice())
        print(player.getPlayerName() + " rolled a " + str(move))
        player.movePlayer(move, len(self.board))
        #self.board[player.playerLocation].landAction(player)


playerInfo = [("Chris", "Car"), ("Kolbe", "Boat")]
game = Monopoly(playerInfo)
game.playerTurn(game.players[0])
print(game)


