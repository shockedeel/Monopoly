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
                    TaxProperty(propertyInfo[0], int(propertyInfo[4]), bool(propertyInfo[2]), float(propertyInfo[3])))

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
                board.append(UtilityProperty(propertyInfo[0], int(propertyInfo[2]), int(propertyInfo[2])/2))

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
        self.cards = []

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

    def countPropertiesOfType(self, typez):
        count = 0
        for property in self.properties:
            if type(property) == typez:
                count += 1
        return count

    def cantPay(self):
        pass #TODO need to add this. Handles banckruptcy

    def payMoney(self, amount):
        if self.wallet - amount < 0:return False
        self.wallet -= amount
        return True

    def calculateTotalPropertyValue(self):
        totalPropValue = 0
        for prop in self.properties:
            totalPropValue += prop.getPrice()
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

        if self.playerLocation < 0:
            self.playerLocation = 40 + self.playerLocation

    def moveToLocation(self, location):
        self.playerLocation = location

    def addCard(self, card):
        self.cards.append(card)


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

    def landAction(self, player):
        player.receiveMoney(400)


class ChanceProperty(Property):
    def __init__(self, name):
        super().__init__(name)

    def landAction(self, player, deck):
        card = deck.drawCard()
        print(card)
        return card.handleCard(player)


class CommunityChestProperty(Property):
    def __init__(self, name):
        super().__init__(name)

    def landAction(self, player, deck):
        card = deck.drawCard()
        print(card)
        return card.handleCard(player)


class JailProperty(Property):
    def __init__(self, name):
        super().__init__(name)

    def landAction(self, player):
        pass


class GoJailProperty(Property):
    def __init__(self, name):
        super().__init__(name)

    def landAction(self, player):
        player.moveToLocation(10)
        return


class FreeParkingProperty(Property):
    def __init__(self, name):
        super().__init__(name)
        self.potValue = 0

    def landAction(self, player):
        player.receiveMoney(self.potValue)
        self.potValue = 0
        return


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

    def getRentPrice(self):
        count = self.owner.countPropertiesOfType(RailProperty)
        if count == 1: return 25
        if count == 2: return 50
        if count == 3: return 100
        if count == 4: return 200


    def landAction(self, player, toBuy):
        if self.owner == None:
            if player.getWallet() - self.getPrice() < 0:
                pass
            else:
                if bool(toBuy):
                    player.payMoney(self.getPrice())
                    player.getProperty(self)
                    self.owner = player
                else: pass

        elif self.owner != player.getPlayerName():
            if player.getWallet() - self.getPrice() < 0:
                player.cantPay()
            else:
                player.payMoney(self.getRentPrice())
                self.owner.receiveMoney(self.getRentPrice())


class UtilityProperty(RailProperty):
    def __init__(self, name, price, mortgageAmount):
        super().__init__(name, price, mortgageAmount)

    def __str__(self):
        return super().__str__() + " " + str(self.propertyPrice)

    def getRentPrice(self):
        count = self.owner.countPropertiesOfType(UtilityProperty)
        if count == 1: multiplier = 4
        else: multiplier = 10
        # Note: Instead of passing in a dice class just add an impromptu version
        roll = random.randint(1, 6) + random.randint(1, 6)
        return roll * multiplier

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
        return self.rentTuple[self.houseCount]

    def getHouseCount(self):
        return self.houseCount



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
                player.payMoney(int(self.variableRate * player.calculateTotalPropertyValue()))
            else:
                player.payMoney(self.taxAmount)
        else:
            player.payMoney(self.taxAmount)


class Deck:
    def __init__(self, kind):
        self.index = 0
        self.deck = self.fillDeck(kind)
        self.shuffleDeck()
    def __str__(self):
        print(self.deck)

    def fillDeck(self, kind):
        deck = []
        if kind == "community":
            f = open("CommunityChest.txt")
        else: f = open("Chance.txt")

        # Add Cards to Deck
        for line in f:
            line = line[:-1]
            cardInfo = tuple(line.split('*'))
            if cardInfo[1] == "moveTo": deck.append(MoveToCard(cardInfo[0], int(cardInfo[2])))
            if cardInfo[1] == "nearest": deck.append(NearestCard(cardInfo[0], cardInfo[2]))
            if cardInfo[1] == "make": deck.append(MakeCard(cardInfo[0], int(cardInfo[2])))
            if cardInfo[1] == "getOut": deck.append(GetOutCard(cardInfo[0]))
            if cardInfo[1] == "move": deck.append(MoveCard(cardInfo[0], int(cardInfo[2])))
            if cardInfo[1] == "house": deck.append(HouseCard(cardInfo[0], int(cardInfo[2]), int(cardInfo[3])))
            if cardInfo[1] == "pay": deck.append(PayCard(cardInfo[0], int(cardInfo[2]), bool(cardInfo[3])))
        return deck

    def shuffleDeck(self):
        random.shuffle(self.deck)
        self.index = 0

    def drawCard(self):
        if self.index == len(self.deck) - 1:
            self.index = 0
        card = self.deck[self.index]
        self.index += 1
        return card


class CommunityChestDeck(Deck):
    def __init__(self, kind):
        super().__init__("community")


class ChanceDeck(Deck):
    def __init__(self, kind):
        super().__init__("chance")


class Card:
    def __init__(self, description):
        self.description = description

    def __str__(self):
        return self.description

    def __repr__(self):
        return str(self)


class MoveToCard(Card):
    def __init__(self, description, index):
        super().__init__(description)
        self.index = index

    def handleCard(self, player):
        player.moveToLocation(self.index)


class MoveCard(Card):
    def __init__(self, description, moveAmount):
        super().__init__(description)
        self.moveAmount = moveAmount

    def handleCard(self, player):
        player.movePlayer(self.moveAmount, 39)


class NearestCard(Card):
    def __init__(self, description, destinationType):
        super().__init__(description)
        self.destinationType = destinationType

    def handleCard(self, player):
        pass #TODO Find Nearest Utility or Rail and Double.


class GetOutCard(Card):
    def __init__(self, description):
        super().__init__(description)

    def handleCard(self, player):
        player.addCard(self)


class HouseCard(Card):
    def __init__(self, description, houseAmount, hotelAmount):
        super().__init__(description)
        self.houseChargeAmount = houseAmount
        self.hotelChargeAmount = hotelAmount

    def handleCard(self, player):
        houses = 0
        hotels = 0
        for prop in player.properties:
            if type(prop) == ColorProperty:
                if prop.houseCount == 5: hotels += 1
                else: houses += prop.houseCount
        player.payMoney(houses * self.houseChargeAmount + hotels * self.hotelChargeAmount)


class PayCard(Card):
    def __init__(self, description, amount, payAll):
        super().__init__(description)
        self.amount = amount
        self.payAll = payAll

    def handleCard(self, player):
        if self.payAll:
            pass #TODO Need to figure out a way to pay all players
        else: player.payMoney(self.amount)


class MakeCard(Card):
    def __init__(self, description, amount):
        super().__init__(description)
        self.amount = amount

    def handleCard(self, player):
        player.receiveMoney(self.amount)


class CollectCard(Card):
    def __init__(self , description, amount):
        super().__init__(description)
        self.amount = amount

    def handleCard(self, player):
        pass #TODO Need to get money from all players


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
        self.communityChest = CommunityChestDeck("community")
        self.chance = ChanceDeck("chance")

    def __str__(self):
        string = ""
        for player in self.players:
            string += "(" + str(player) + ", " + str(self.board.getPropertyName(player.playerLocation)) + ") "
        return string

    def playerTurn(self, player):
        dice = Dice()
        while True:
            # Roll Dice and move Player
            die1, die2 = dice.rollDice()

            # Handle case if 3 doubles have been rolled
            if dice.doublesCount == 3:
                player.moveToLocation(10)
            move = die1 + die2
            player.movePlayer(move, len(self.board) - 1)

            # Land on property and do said action.
            prop = self.board[player.playerLocation]
            print(player.getPlayerName() + " rolled a " + str(move) + " and is on " + prop.getName())

            while True:
                # Store player location to check to see if they landed on chance and moved locations to do new land action.
                playerLocation = player.playerLocation

                if type(prop) == CommunityChestProperty:
                    prop.landAction(player, self.communityChest)
                elif type(prop) == ChanceProperty:
                    prop.landAction(player, self.chance)
                elif type(prop) == ColorProperty or type(prop) == RailProperty or type(prop) == UtilityProperty:
                    prop.landAction(player, True) #TODO get input

                if playerLocation == player.playerLocation:
                    break

            # Handle doubles case
            if die1 != die2:
                print("Turn Over \n")
                break

            print()

    def completeTurn(self):
        for player in self.players:
            self.playerTurn(player)

    def playXRounds(self,x):
        for x in range(x):
            self.completeTurn()

playerInfo = [("Chris", "Car"), ("Kolbe", "Boat")]
game = Monopoly(playerInfo)
game.playXRounds(90)
print(game)


