import pdb
from player import Player
from heartsgame import HeartsGame
from common import *

#printOn = False

playerNorth = Player("North")
playerEast = Player("East")
playerSouth = Player("South")
playerWest = Player("West")
allPlayers = [playerNorth, playerEast, playerSouth, playerWest]
theGame = HeartsGame(allPlayers, printOn)

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

if printOn:
	print "\nFinal score:"
	print "North: "+str(playerNorth.totalScore)
	print "East: "+str(playerEast.totalScore)
	print "South: "+str(playerSouth.totalScore)
	print "West: "+str(playerWest.totalScore)

print "...running games... (%d games took %.03f seconds)" % (numRounds, t.interval)

# Get the winner from all the games played
def winner(players):
	winner = players[0]
	for player in players:
		if player.totalScore > winner.totalScore:
			winner = player
	return winner
winner = winner(allPlayers)

# If desired, print moves of winner
printWinner = False
if printWinner:
	print "\nWinner: "+str(winner)+"\n"+(15*"-")+"\nAll their moves: \n"+(15*"-")
	for move in winner.moves:
		for key, value in move.iteritems():
			key+=":"
			if len(key) < 8: key+="     "
			print str(key)+"\t" + str(value)
		print "\n"

# Now write all input, output vectors to file in csv format
writeWinner = True
if writeWinner:
	writeFile = open('../heartsMoves.csv', 'w')
	# first print out header values
	prefix = ""
	for key, value in winner.moves[0].iteritems():
		if key == "Input Vector" or key == "Output Vector":
			for vectorKey, vectorValue in value.iteritems():
				writeFile.write("%s%s" % (prefix, str(vectorKey)))
				prefix = ", "
	writeFile.write("\n")


	# loop through moves
	for move in winner.moves: 
		#loop through parts of move
		prefix = ""
		for key, value in move.iteritems(): 
			# If we're looking at input or output vectors,
			# loop through the values in the vector
			if key == "Input Vector" or key == "Output Vector":
				for vectorKey, vectorValue in value.iteritems():
					writeFile.write("%s%s" % (prefix, str(vectorValue)))
					prefix = ","
		writeFile.write("\n")
	writeFile.close()

