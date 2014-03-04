from pybrain.datasets            import ClassificationDataSet
from pybrain.tools.shortcuts 	 import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer

import csv
import pdb
import pickle
import common
from common import Timer

filename = common.netWriteFilename

def main():
	# Declare length of input and output vectors here, to change later
	lenInput = 6
	lenOutput = 4
	lenHidden = 8 # change this?
	labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

	# Initialize data set used for training
	data = ClassificationDataSet(lenInput, lenOutput, class_labels=labels)

	# Get input and output vectors from file, build dataset
	with open('../heartsMoves.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=",", quotechar="|")
		firstLine = True
		for row in reader:
			if firstLine:
				labels = row
			if not firstLine:
				rowInput = map(float,row[:lenInput])
				rowOutput = map(float, row[lenInput:])
				#pdb.set_trace()
				data.addSample(rowInput, rowOutput)
			firstLine = False

	##########################################
	# DATASET IS BUILT, NOW TRAIN NEURAL NET #
	##########################################

	# build network
	fnn = buildNetwork(lenInput, lenHidden, lenOutput)
	# train it with data
	trainer = BackpropTrainer(fnn, dataset=data, momentum=.1, verbose=False, weightdecay=0.01)
	trainer.trainOnDataset(data)

	#print 'final weights:', fnn.params

	####################################
	# NET IS TRAINED, NOW SAVE TO DISK #
	####################################

	fileObject = open(filename, 'w')
	pickle.dump(fnn, fileObject)
	fileObject.close()

if  __name__ =='__main__':

    with Timer() as t:
    	main()

    print "...training... (took %.03f seconds)" % t.interval
    print "wrote to %s" % filename

