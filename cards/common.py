from suitrank import Suit, Rank
import time
import os.path

numRounds = 1

printOn = False
# Look to txt file to see if program should print
if os.path.exists("savedNets/shouldPrint.txt"):
	printOn = True

# Grab number of trainedNet from file containing it
netCountFile = "savedNets/netNumber.txt"
fileNum = open(netCountFile, 'r').readlines()[-1].strip()

netWriteFilename = "savedNets/savedNet%s.p" % fileNum
netReadFilename = None
if fileNum != "0":
	netReadFilename = "savedNets/savedNet%d.p" % (int(fileNum) - 1)


# Prints a line of dots
def printline():
	print "."*45

# Returns list of cards as formatted string
def cardsToStringList(cards):
	cards_string = []
	for card in cards:
		cards_string.append(str(card))
	return cards_string

# Get the number of cards for a specific card
def getPointsOfCard(card):
	if card.getSuit() == Suit.Hearts:
		return 1
	if card.getSuit() == Suit.Spades and card.getRank() == Rank.Queen:
		return 13
	return 0

# Return the index of the winner of a trick
def winnerOfTrick(trick):
	# figure out which card wins
	ledSuit = trick[0].getSuit()
	cardsInSuit = [trick[0]]
	# add rest of the cards that are of same suit
	for card in trick[1:]:
		if card.getSuit() == ledSuit:
			cardsInSuit.append(card)
	# now find highest one
	if len(cardsInSuit) == 1:
		return trick.index(cardsInSuit[0])
	winningCard = trick[0]
	for card in cardsInSuit:
		if card.getRank > winningCard.getRank:
			winningCard = card
	return trick.index(winningCard)	

# Timer class to record how long iterations take
class Timer:    
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start
