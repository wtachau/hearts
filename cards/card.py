from suitrank import Suit, Rank

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
