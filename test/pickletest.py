
# Save a dictionary into a pickle file.
import pickle

def a():
	print "hello"

#favorite_color = { "lion": "yellow", "kitty": "red" }

pickle.dump( a, open( "save.p", "wb" ) )