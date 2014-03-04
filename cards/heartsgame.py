from suitrank import Suit, Rank
from card import Card
from gamestate import GameState
from deck import Deck
from common import *

# Represents the whole game
class HeartsGame:
	def __init__(self, players, printOn):
		self.thePlayers = players
		self.printOn = printOn

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


	# Method to start the game
	def playGame(self):

		def pointsInTrick(cards):
			numPoints = 0
			for card in cards:
				numPoints += getPointsOfCard(card)
			return numPoints

		gameState = GameState()

		gameOver = False
		# keep going until a player gets 100
		while not gameOver:
			self.theDeck = Deck()
			self.theDeck.shuffle()
			self.dealCards()

			for i in range(13):
				if self.printOn: print "\n\n\n --- TRICK "+str(i+1)+"---\n\n"
				self.queuePlayers() # set who goes first
				current_trick = []
				# print hards
				if self.printOn:
					for player in self.thePlayers:
						player.printShortHand()

				# get turns from each player
				if self.printOn: 
					printline()
					gameState.printState()
				if self.printOn: printline()
				for player in self.thePlayers:
					playersTurn = player.getTurn(current_trick, gameState)
					current_trick.append(playersTurn)
					if self.printOn: print player.getID()+ " >\tchooses "+str(playersTurn)
					player.setGoesFirst(False) #reset

				# now update game state
				gameState.numTrick += 1
				if ((Card(Suit.Spades, Rank.Queen)) in current_trick):
					gameState.queenPlayed = 1
				if not gameState.heartsBroken:
					for card in current_trick:
						if card.getSuit() == Suit.Hearts:
							gameState.heartsBroken = 1


				# Now handle who won the trick
				winningIndex = winnerOfTrick(current_trick)
				if self.printOn: 
					print "        * " + str(self.thePlayers[winningIndex].getID()) + " wins with a "+ \
							str(current_trick[winningIndex])
					printline()
				self.thePlayers[winningIndex].addPoints(pointsInTrick(current_trick))
				self.thePlayers[winningIndex].setGoesFirst(True)

				# print out scores 
				if self.printOn:
					for player in self.thePlayers:
						print str(player.getID()) + ": "+str(player.getPoints())

			## AT THE END OF EVERY ROUND

			# Find out if any player has 100
			for player in self.thePlayers:
				if player.getPoints() >= 100:
					gameOver = True

			# reset who goes first (goesFirst will be set in dealCards)
			for player in self.thePlayers:
				player.setGoesFirst(False)

			# and reset trick #
			gameState.reset()

		## AT THE END OF THE GAME 

		# at end of game, find winner and reset player state
		winner = self.thePlayers[0]
		for player in self.thePlayers:
			if player.getPoints() < winner.getPoints():
				winner = player

		# reset points
		for player in self.thePlayers:
			player.points = 0

		if self.printOn:
			print "GAME OVER: %s WINS!" % str(winner.getID())
			
		return winner