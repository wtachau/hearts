from trainNet import filename, lenInput, makeChoice
import csv
import numpy
import pickle

# inputs for testing
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
predictions = numpy.empty_like(outputs)

# (Try to) get the predict method from the neural net!
neuralnet = pickle.load(open(filename, "rb" ))

print inputs
print outputs

#choose(inputs, predictions)

print predictions
