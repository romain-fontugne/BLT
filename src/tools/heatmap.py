import matplotlib
import numpy as np
matplotlib.use("AGG")
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
def heatmap(data, row_labels, column_labels):
    fig, ax = plt.subplots()
    #heatmap = ax.pcolor(data, cmap=plt.cm.Blues)
    #ax.set_xticks(np.arange(data.shape[0]) + 0.5, minor=False)
    #ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)

    #ax.invert_yaxis()
    #ax.xaxis.tick_top()

    #ax.set_xticklabels(row_labels, minor=False)
    #ax.set_yticklabels(column_labels, minor=False)
    plt.imshow(data, aspect='auto', interpolation='none',
                       cmap=plt.get_cmap("bwr"), vmin=-1.0, vmax=1.0)
    plt.colorbar()
    plt.xticks(range(data.shape[1]), row_labels)
    plt.yticks(range(data.shape[0]), column_labels)
    plt.gca().get_xaxis().set_ticks_position('none')
    plt.gca().get_yaxis().set_ticks_position('none')
    plt.savefig("heatmap.png")

    return heatmap

f = open("correlation.txt", "r")
data = list()

for line in f:
    data.append([float(x) for x in line.split()])

data = np.array(data)
label = ["DA", "NP", "AC", "PC", "CC", "DW", "PP","OC","RP"] 
heatmap(data, label, label)
