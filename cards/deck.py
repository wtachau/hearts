from card import Card
from random import shuffle

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