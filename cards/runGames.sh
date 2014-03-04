#!/bin/bash

FILENAME="savedNets/netNumber.txt"
PRINTFILENAME="savedNets/shouldPrint.txt"
ITERATIONS=10
COUNTER=0

# first delete all savedNets, counter, and print indicator
rm savedNets/savedNet* && rm $FILENAME && rm $PRINTFILENAME

# Loop through #iterations number of times
while [ $COUNTER -lt $ITERATIONS ]; do

	echo -e "\n------------------\n"

	# save iteration number to file
	echo $COUNTER >> $FILENAME

	# main.py
	# * Plays games
	# * Trains from net if exists
	# * Saved moves to .csv
	python main.py

	# trainNet.py
	# * trains neural net 
	# * based off moves in csv
	# * writes to file determined above
	python trainNet.py

	# Increase net number
	let COUNTER=COUNTER+1 
done

# write a cap to the netNumber list, so next program trains off correct net
echo $ITERATIONS >> $FILENAME
# put something in print indicator file, so program prints
echo "yes" > $PRINTFILENAME


echo -e "\n ---------------------\n"
echo "PLAYING A GAME -> SHOW RESULTS:"
python main.py
