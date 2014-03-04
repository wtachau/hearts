import pickle
import card
import common
from random import choice
import os.path

import pdb

printOn = common.printOn
random = False

# Check if file (trained Net) exists.
# If so, train off it.
# If not, this is the first iteration, so be random
if common.netReadFilename != None: 
	fileObject = open(common.netReadFilename, 'r')
	net = pickle.load(fileObject)
	print ">> training from %s" % common.netReadFilename
	random=False
else:
	print ">> first go around, random"
	random=True

def getCard(inputLayer, eligibleCards):
	# If this is the first round, choice is random
	if random:
		return choice(eligibleCards)
	# Every subsequent round, train from saved net
	else:
		output = net.activate(inputLayer)
		# based on output, choose a card
		ofLedSuit = output[0]
		pointsOfCard = output[1] * 13 # was scaled down
		rank = output[2]
		wouldWin = output[3]

		if printOn:
			print "ofLedSuit: %.02f \tpoints: %.02f \t rank: %.02f \t wouldWin: %.02f" % (ofLedSuit, pointsOfCard, rank, wouldWin)
			print common.cardsToStringList(eligibleCards)
			
		# for now, still random
		return choice(eligibleCards)


#getCard((0, 0, 0, 0.07692308, 1, 1,))
#getCard((1, .667, 1, .92, 0, .667 ))