from enum import Enum
from random import choice
from random import shuffle
import pdb
import operator
import time

class Timer:    
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start

def printline():
	print "."*45

def cardsToStringList(cards):
	cards_string = []
	for card in cards:
		cards_string.append(str(card))
	return cards_string

# enum of Suit
class Suit(Enum):
	Clubs = 0
	Diamonds = 1
	Spades = 2
	Hearts = 3

# enum of Rank
class Rank(Enum):
	Two = 1
	Three = 2
	Four = 3
	Five = 4
	Six = 5
	Seven = 6
	Eight = 7
	Nine = 8
	Ten = 9
	Jack = 10
	Queen = 11
	King = 12
	Ace = 13

# Represents a Playing Card
class Card:

	suit_names = ['Clubs', 'Diamonds', 'Spades', 'Hearts']
	rank_names = [None, '2', '3', '4', '5', '6', '7', 
			  '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

	def __init__(self, suit, rank):
		self.theSuit = suit
		self.theRank = rank

	# custom string for card, i.e. "Jack of Hearts"
	def __str__(self):
		return '%s of %s' % (Card.rank_names[self.theRank],
							 Card.suit_names[self.theSuit])

	def __eq__(self, card):
		return self.theSuit == card.theSuit and self.theRank == card.theRank

	def __getitem__(self,index):
		if index == 0:
			return self.theSuit
		else:
			return self.theRank


	def shortHand(self):
		card_string = ""
		# first number
		if self.theRank	== Rank.Ace:
			card_string += "A-"
		elif self.theRank == Rank.Two:
			card_string += "2-"
		elif self.theRank == Rank.Three:
			card_string += "3-"
		elif self.theRank == Rank.Four:
			card_string += "4-"
		elif self.theRank == Rank.Five:
			card_string += "5-"
		elif self.theRank == Rank.Six:
			card_string += "6-"
		elif self.theRank == Rank.Seven:
			card_string += "7-"
		elif self.theRank == Rank.Eight:
			card_string += "8-"
		elif self.theRank == Rank.Nine:
			card_string += "9-"
		elif self.theRank == Rank.Ten:
			card_string += "10-"
		elif self.theRank == Rank.Jack:
			card_string += "J-"
		elif self.theRank == Rank.Queen:
			card_string += "Q-"
		elif self.theRank == Rank.King:
			card_string += "K-"
		# then suit
		if self.theSuit == Suit.Spades:
			card_string += "Sp."
		elif self.theSuit == Suit.Hearts:
			card_string += "Ht."
		elif self.theSuit == Suit.Diamonds:
			card_string += "Di."
		elif self.theSuit == Suit.Clubs:
			card_string += "Cl."

		return card_string+"\t"

	def getSuit(self):
		return self.theSuit

	def getRank(self):
		return self.theRank

# Represents a Deck
class Deck:
	def __init__(self):
		self.deck = self.makeDeck()

	# Generate the deck
	def makeDeck(self):
		deck = []
		for i, suit in enumerate(Card.suit_names):
			for j, rank in enumerate(Card.rank_names[1:]):
				deck.append(Card(i,j+1)) # j + 1 because we ignore 0
		return deck

	def popCard(self):
		return self.deck.pop()

	def size(self):
		return len(self.deck)

	def shuffle(self):
		shuffle(self.deck)

# Represents a the current state of the game
class GameState:
	def __init__(self):
		self.heartsBroken = False
		self.queenPlayed = False
		self.numTrick = 1 

	def getDict(self):
		gamestatedict = {}
		gamestatedict['heartsBroken'] = self.heartsBroken
		gamestatedict['queenPlayed'] = self.queenPlayed
		gamestatedict['numTrick'] = self.numTrick
		return gamestatedict


	def printState(self):
		print "Hearts broken: "+str(self.heartsBroken)
		print "Queen played: "+str(self.queenPlayed)
		print "Trick number: "+str(self.numTrick)

# Represents a Player
class Player: 

	def __init__(self, id_num):
		self.id = id_num
		self.goesFirst = False
		self.points = 0
		self.totalScore = 0
		self.moves = []

	def __str__(self):
		return self.id

	def getMoves(self):
		return self.moves

	def reset(self):
		self.goesFirst = False
		self.points = 0

	def setHand(self, cards):
		self.hand = sorted(cards, key=operator.itemgetter(0,1)) # sort cards based on attributes
		if Card(Suit.Clubs, Rank.Two) in cards:
			self.goesFirst = True

	def doesGoFirst(self):
		return self.goesFirst

	def setGoesFirst(self, goesFirst):
		self.goesFirst = goesFirst

	# Decide which card to play.
	# Arguably the point of the whole project.
	def getTurn(self, trickSoFar, gameState):
		# use trick so far to determine what trick

		# GET ELIGIBLE CARDS
		eligibleCards = []
		# If it's the first trick
		if gameState.numTrick == 1 and trickSoFar == []: # first lead: must have two of clubs
			self.hand.remove(Card(Suit.Clubs, Rank.Two))
			return Card(Suit.Clubs, Rank.Two)
		# if it's the first trick for everyone else
		elif gameState.numTrick == 1:
			for card in self.hand:
				if card.getSuit() == Suit.Clubs:
					eligibleCards.append(card)
			if eligibleCards == []: # if you don't have clubs, no 'bleeding' on first trick
				for card in self.hand:
					if card.getSuit() != Suit.Hearts and \
						(card.getSuit() != Suit.Spades or card.getRank() != Rank.Queen):
						eligibleCards.append(card)
		# else if you're leading for every other trick
		elif trickSoFar == []: 
			# hearts is not broken
			if not gameState.heartsBroken:
				for card in self.hand:
					if card.getSuit() != Suit.Hearts:
						eligibleCards.append(card)
				def allHearts(cards):
					isAllHearts = True
					for card in cards:
						if card.getSuit() != Suit.Hearts:
							return False
					return True
				# unless you have no options... (assert that it is all hearts)
				if eligibleCards == [] and allHearts(self.hand):
					eligibleCards = self.hand
			else:
				eligibleCards = self.hand
		# if you're following the second or later trick
		else:
			ledSuit = trickSoFar[0].getSuit()
			for card in self.hand:
				if card.getSuit() == ledSuit:
					eligibleCards.append(card)
			if len(eligibleCards) == 0: # if you don't have any of the led suit
				eligibleCards = self.hand

		# At this point the eligible cards to choose from are set

		# If only one option, play it. Otherwise... choose randomly (for now)
		if len(eligibleCards) == 1:
			cardToPlay = eligibleCards[0]
		else:
			#
			# HERE'S WHERE THE MAGIC HAPPENS
			#
			cardToPlay = choice(eligibleCards)

		# "remember" it to learn from later
		self.moves.append({
			"trick": cardsToStringList(trickSoFar), 
			"game state": gameState.getDict(), 
			"hand":cardsToStringList(self.hand), 
			"choice":str(cardToPlay)
			})

		# remove it from hand, and play it
		self.hand.remove(cardToPlay)
		return cardToPlay

	def printShortHand(self):
		hand_string = self.id + ":\t"
		for card in self.hand:
			hand_string += card.shortHand()
		print hand_string

	def getID(self):
		return self.id

	def addPoints(self, points):
		self.points += points

	def getPoints(self):
		return self.points

# Represents the whole game
class HeartsGame:
	def __init__(self, players):
		self.thePlayers = players

	# Reorganize the players based on which goes first
	def queuePlayers(self):
		newPlayerOrder = []
		for index, player in enumerate(self.thePlayers):
			if player.doesGoFirst():
				newPlayerOrder+=self.thePlayers[index:]
				newPlayerOrder+=self.thePlayers[:index]
				break
		self.thePlayers = newPlayerOrder

	# pop all cards off deck and distribute them to players' hands
	def dealCards(self):
		p0 = []
		p1 = []
		p2 = []
		p3 = []

		while(self.theDeck.size() > 0):
			dealTo = self.theDeck.size() % 4
			if dealTo == 0:
				p0.append(self.theDeck.popCard())
			elif dealTo == 1:
				p1.append(self.theDeck.popCard())
			elif dealTo == 2:
				p2.append(self.theDeck.popCard())
			else:
				p3.append(self.theDeck.popCard())

		self.thePlayers[0].setHand(p0)
		self.thePlayers[1].setHand(p1)
		self.thePlayers[2].setHand(p2)
		self.thePlayers[3].setHand(p3)

	def winnerOfTrick(self, trick):
		# figure out which card wins
		ledSuit = trick[0].getSuit()
		cardsInSuit = [trick[0]]
		# add rest of the cards that are of same suit
		for card in trick[1:]:
			if card.getSuit() == ledSuit:
				cardsInSuit.append(card)
		# now find highest one
		winningCard = trick[0]
		if len(cardsInSuit) == 1:
			return trick.index(cardsInSuit[0])
		for card in cardsInSuit:
			if card.getRank > winningCard.getRank:
				winningCard = card
		return trick.index(winningCard)	

	# Method to start the game
	def playGame(self):

		def pointsInTrick(cards):
			numPoints = 0
			for card in cards:
				if card.getSuit() == Suit.Hearts:
					numPoints += 1
				if card.getSuit() == Suit.Spades and card.getRank() == Rank.Queen:
					numPoints += 13
			return numPoints


		self.theDeck = Deck()
		self.theDeck.shuffle()
		self.dealCards()

		gameState = GameState()

		for i in range(13):
			if printOn: print "\n\n\n --- TRICK "+str(i+1)+"---\n\n"
			self.queuePlayers() # set who goes first
			current_trick = []
			# print hards
			if printOn:
				for player in self.thePlayers:
					player.printShortHand()

			# get turns from each player
			if printOn: 
				printline()
				gameState.printState()
			if printOn: printline()
			for player in self.thePlayers:
				playersTurn = player.getTurn(current_trick, gameState)
				current_trick.append(playersTurn)
				if printOn: print player.getID()+ " >\tchooses "+str(playersTurn)
				player.setGoesFirst(False) #reset

			# now update game state
			gameState.numTrick += 1
			if ((Card(Suit.Spades, Rank.Queen)) in current_trick):
				gameState.queenPlayed = True
			if not gameState.heartsBroken:
				for card in current_trick:
					if card.getSuit() == Suit.Hearts:
						gameState.heartsBroken = True


			# Now handle who won the trick
			winningIndex = self.winnerOfTrick(current_trick)
			if printOn: 
				print "        * " + str(self.thePlayers[winningIndex].getID()) + " wins with a "+ \
						str(current_trick[winningIndex])
				printline()
			self.thePlayers[winningIndex].addPoints(pointsInTrick(current_trick))
			self.thePlayers[winningIndex].setGoesFirst(True)

			# print out scores 
			if printOn:
				for player in self.thePlayers:
					print str(player.getID()) + ": "+str(player.getPoints())

		# at end of game, find winner and reset player state
		winner = self.thePlayers[0]
		for player in self.thePlayers:
			if player.getPoints() < winner.getPoints():
				winner = player
		# now reset
		for player in self.thePlayers:
			player.reset()
		return winner


printOn = False
numRounds = 100

playerNorth = Player("North")
playerEast = Player("East")
playerSouth = Player("South")
playerWest = Player("West")
allPlayers = [playerNorth, playerEast, playerSouth, playerWest]
theGame = HeartsGame(allPlayers)

with Timer() as t:
	for i in range(numRounds):
		winner = theGame.playGame()
		if winner == playerNorth:
			playerNorth.totalScore += 1
		elif winner == playerEast:
			playerEast.totalScore += 1
		elif winner == playerSouth:
			playerSouth.totalScore += 1
		else:
			playerWest.totalScore += 1

		# print out progress
		if (numRounds > 100):
			percentInc = .10 #change this to % increment you want
			if i % (percentInc*numRounds) == 0:
				print str(i/(numRounds/100))+"%"

print "\nFinal score:"
print "North: "+str(playerNorth.totalScore)
print "East: "+str(playerEast.totalScore)
print "South: "+str(playerSouth.totalScore)
print "West: "+str(playerWest.totalScore)

print "%d games took %.03f seconds" % (numRounds, t.interval)

def winner(players):
	winner = players[0]
	for player in players:
		if player.totalScore > winner.totalScore:
			winner = player
	return winner
winner = winner(allPlayers)

print "\nWinner: "+str(winner)+"\n"+(15*"-")+"\nAll their moves: \n"+(15*"-")
for move in winner.moves:
	print move
