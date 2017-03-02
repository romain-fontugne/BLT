import pickle

def load_pickle(pickle_file):
	with open(pickle_file, mode="rb") as f:
	    pkl_data = pickle.load(f)
	f.close
	return pkl_data
