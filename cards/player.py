import operator
from card import Card
from suitrank import Suit, Rank
from common import *
from predict import getCard

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

	def setHand(self, cards):
		self.hand = sorted(cards, key=operator.itemgetter(0,1)) # sort cards based on attributes
		if Card(Suit.Clubs, Rank.Two) in cards:
			self.goesFirst = True

	def doesGoFirst(self):
		return self.goesFirst

	def setGoesFirst(self, goesFirst):
		self.goesFirst = goesFirst

	# Based on the current hand and game state, generate vector
	# to represent "what kind" of situation user is in
	def getInputVector(self, eligibleCards, trickSoFar, gameState):
		# Include all gamestate values
		inputVector= gameState.getDict() 

		# How many points are in the hand so far
		maxPointsPossible = 15
		pointsSoFar = 0
		for eachCard in trickSoFar:
			pointsSoFar+= getPointsOfCard(eachCard)
		inputVector['pointsSoFar'] = float(pointsSoFar)/float(maxPointsPossible)

		# How many cards have been played in the trick so far
		maxCardsPossible = 3
		inputVector['cardsPlayed'] = float(len(trickSoFar))/float(3)

		# Whether user is able to play in the led suit
		ledSuitMetric = 0 # AGAIN - what if this doesn't apply?
		if len(trickSoFar) > 0 and eligibleCards[0].theSuit == trickSoFar[0].theSuit:
			ledSuitMetric = 1
		inputVector["canPlayInLedSuit"]=float(ledSuitMetric)

		return inputVector

	# Based on the current situation and given a card, generate vector
	# to represent "what kind" of card was chosen
	def getOutputVector(self, card, eligibleCards, trickSoFar, gameState):
		outputVector = {}
		
		# How high the card is relative to all possible cards
		rankMetric = 0 # POSSIBLE FIX: what should this value be when len(eligibleCards) = 1?
		if len(eligibleCards) > 1:
			# first sort by rank
			eligibleCardsSorted = sorted(eligibleCards, key=operator.itemgetter(1))
			rankMetric = float(eligibleCardsSorted.index(card))/float(len(eligibleCards)-1)
		outputVector['rank']=rankMetric

		# If user plays same suit as was led
		ledSuitMetric = 0 # AGAIN - what if this doesn't apply?
		if len(trickSoFar) > 0 and card.theSuit == trickSoFar[0].theSuit:
			ledSuitMetric = 1
		outputVector["ofLedSuit"]=float(ledSuitMetric)

		# How many points it was worth 
		maxPossiblePoints = 13
		outputVector['pointsOfCard']= float(getPointsOfCard(card))/float(maxPossiblePoints)

		# If it would win the current trick
		wouldBeTrick = trickSoFar + [card]
		wouldWinTrick = 0
		if winnerOfTrick(wouldBeTrick) == wouldBeTrick.index(card):
			wouldWinTrick = 1
		outputVector['wouldWin'] = float(wouldWinTrick)

		return outputVector
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

		## 
		## Generate Input Vector - this represents the game state. 
		## Used for:
		##   * determining what card to play
		##   * saving for future training
		##
		gameInputVector = self.getInputVector(eligibleCards, trickSoFar, gameState)

		# If only one option, play it. Otherwise... choose randomly (for now)
		if len(eligibleCards) == 1:
			if printOn:
				print "\n\n"
				print "** only one choice"
			cardToPlay = eligibleCards[0]
		else:
			#
			# HERE'S WHERE THE MAGIC HAPPENS
			#

			#print gameInputVector.values()
			if printOn:
				print "\n\n"
				print "trick >>>  \t"  + str(cardsToStringList(trickSoFar))
				print "inputVector >>>\t" + str(gameInputVector)
				print "in hand >>> \t" + str(cardsToStringList(eligibleCards))
			cardToPlay = getCard(gameInputVector.values(), eligibleCards)

		# "remember" it to learn from later
		self.moves.append({
				"trick": cardsToStringList(trickSoFar),
				"hand":cardsToStringList(self.hand), 
				"eligibleCards":cardsToStringList(eligibleCards),
				"choice":str(cardToPlay),
				"Input Vector":gameInputVector,
				"Output Vector":self.getOutputVector(cardToPlay, eligibleCards, trickSoFar, gameState)
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