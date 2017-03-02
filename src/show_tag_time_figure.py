import matplotlib
matplotlib.use("AGG")
from matplotlib import pyplot as plt
import numpy as np
import argparse
import pickle
from load_pickle import load_pickle
import matplotlib.ticker as ticker


parser = argparse.ArgumentParser()
parser.add_argument("pickle_file", nargs = "*")
args = parser.parse_args()

def save_figure(tags):
    tag = dict()
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    for tagd in sorted(tags.items(), key = lambda x: x[0]):
        for item in tagd[1].items():
            if item[0] not in tag:
                tag[item[0]] = list()
            tag[item[0]].append(item[1])
    for t in tag.items():
        print t
        print t[1]
        print sorted(tags.keys())
        ax.plot(sorted(tags.keys()), t[1], label = t[0])

        #ax.plot(np.array([1,2,3,4,5]), t[1])
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    ax.get_xaxis().set_major_locator(ticker.MaxNLocator(integer=True))
    lgnd = plt.legend(bbox_to_anchor=(1.05, 0), loc='lower left', borderaxespad=0)
    #ax.set_title(' test ')
    ax.set_xlabel("year")
    ax.set_ylabel("the number of tag")
    plt.savefig( "../../Data/graphs/test",bbox_extra_artists=(lgnd,), bbox_inches='tight')
tags = dict()
for pkl in args.pickle_file:
    time = int(pkl.split("/")[-1].split(".")[0][: 4])
    with open(pkl, "rw") as f:
        tag_data = pickle.load(f)
        tags[time] = tag_data

save_figure(tags)
