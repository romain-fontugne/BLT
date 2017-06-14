import matplotlib
import numpy as np
import sys
matplotlib.use("AGG")
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
def heatmap(data, row_labels, column_labels, file_name):
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
    plt.savefig(file_name + "_heatmap.png")

    return heatmap

f = open(sys.argv[1], "r")
data = list()
flag = False
for line in f:
    if line.split()[0] == "1.0":
        flag = True
    if flag == True:
        data.append([float(x) for x in line.split()])
    else:
        label = line.split()
        
file_name = sys.argv[1]
file_name = file_name.split(".txt")[0]
data = np.array(data)
clabel = list()
for l in label:
    print l
    l = l.split("_")
    clabel.append(l[0][0].upper() + l[1][0].upper())
print clabel
#label = ["DA", "NP", "AC", "PC", "CC", "DW", "PP","OC","RP"] 
heatmap(data, clabel, clabel, file_name)
