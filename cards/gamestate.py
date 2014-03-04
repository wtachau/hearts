
# Represents a the current state of the game
class GameState:
	def __init__(self):
		self.reset()

	def reset(self):
		self.heartsBroken = 0
		self.queenPlayed = 0
		self.numTrick = 1 

	def getDict(self):
		gamestatedict = {}
		gamestatedict['heartsBroken'] = float(self.heartsBroken)
		gamestatedict['queenPlayed'] = float(self.queenPlayed)
		maxTricksPossible = 13
		gamestatedict['numTrick'] = float(self.numTrick)/float(maxTricksPossible) # to normalize vector
		return gamestatedict


	def printState(self):
		print "Hearts broken: "+str(self.heartsBroken)
		print "Queen played: "+str(self.queenPlayed)
		print "Trick number: "+str(self.numTrick)