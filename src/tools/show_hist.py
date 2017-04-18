import pickle
import matplotlib
matplotlib.use("AGG")
from matplotlib import pyplot as plt
import sys
import numpy as np
import matplotlib.ticker as ticker

with open(sys.argv[1], "rb") as f:
    path_length = pickle.load(f)
filename = sys.argv[1].split("/")[-1].split(".")[0]

y_w = np.array(path_length["announce"].values(), dtype = float)
y_w /= np.sum(y_w)


y_d = np.array(path_length["duplicate"].values(), dtype = float)
y_d /= np.sum(y_d)


plt.bar(path_length["announce"].keys(), y_w, width = 1.0, edgecolor = "red", label = "update" , fill=False, lw=2)
plt.bar(path_length["duplicate"].keys(), y_d, width = 1.0, edgecolor = "blue", label = "duplicate announce", fill=False ,lw = 2)
lgnd = plt.legend(bbox_to_anchor=(1.05, 0), loc='lower left', borderaxespad=0)
plt.gca().get_xaxis().set_major_locator(ticker.MaxNLocator(integer=True))
plt.title("AS Path Length in withdraw and in duplicate withdraw")
plt.xlabel("AS Path Length")
plt.ylabel("the number of messages")
plt.savefig( "/home/tktbtk/Data/graphs/histgram_" + filename + ".png",bbox_extra_artists=(lgnd,), bbox_inches='tight')

for p in path_length:
    print p

