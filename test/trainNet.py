import numpy
import cv2
import pickle
import csv

filename = "choice.p"

# Declare length of input and output vectors here, to change later
lenInput = 6
lenOutput = 4
lenHidden = 8 # change this?

# Create an array of desired layer sizes for the neural net
layers = numpy.array([lenInput, lenHidden, lenOutput])

# Create the neural net
# ANN_MLP = Artificial Neural Net MultiLayer Perceptron
neuralnet = cv2.ANN_MLP(layers)

# And predict
def makeChoice(inputs, predictions):
	neuralnet.predict(inputs, predictions)

def main():
	# Construct input and output vector lists
	inputs = []
	outputs = []

	# Get input and output vectors from file
	with open('../heartsMoves.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=",", quotechar="|")
		skipFirstLine = True
		for row in reader:
			if not skipFirstLine:
				# Need to convert each number to float (weird numpy thing)
				inputLine = []
				outputLine = []
				for index, num in enumerate(row):
					if index < lenInput:
						inputLine.append(float(num))
					else:
						outputLine.append(float(num))
				inputs.append(inputLine)
				outputs.append(outputLine)
			skipFirstLine = False

	# Turn input, output vectors into numpy arrays
	inputs = numpy.array(inputs)
	outputs = numpy.array(outputs)

	#
	# Parameters for Learning
	#

	# step size is gradient step size in back-propagation
	step_size = 0.01

	# momentum (?)
	momentum = 0.0

	# Max steps of training
	nsteps = 10000

	# error threshold for halting training
	max_err = 0.0001

	# When to stop: whichever comes first, count or error
	condition = cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS

	# Tuple of termination criteria: first condition, then # steps, then
	# error tolerance second and third things are ignored if not implied
	# by condition
	criteria = (condition, nsteps, max_err)

	# params is a dictionary with relevant things for NNet training.
	params = dict( term_crit = criteria, 
	               train_method = cv2.ANN_MLP_TRAIN_PARAMS_BACKPROP, 
	               bp_dw_scale = step_size, 
	               bp_moment_scale = momentum )


	#
	# Now train the network
	#
	num_iter = neuralnet.train(inputs, outputs,
	                      None, params=params)

	# Create matrix of predictions
	predictions = numpy.empty_like(outputs)

	makeChoice(inputs, predictions)

	# Save the predictor (card chooser) to file
	saveFile = open (filename, 'wb')
	pickle.dump(neuralnet, saveFile)
	saveFile.close()

	"""print inputs
	print 10*"-"
	print outputs
	print 10*"-"
	print predictions"""


if  __name__ =='__main__':
    main()



