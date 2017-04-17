import matplotlib
import sys
matplotlib.use("AGG")
from matplotlib import pyplot as plt
import numpy as np
import argparse
import pickle
from load_pickle import load_pickle
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from datetime import datetime as dt
import pandas as pd
from allrolling_std import *


parser = argparse.ArgumentParser()
parser.add_argument("pickle_file")
args = parser.parse_args()

def save_figure(tags):
    
    tag = dict()
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    pddata = dict()
    for tagd in sorted(tags.items(), key = lambda x: x[0]): # ex) tagd[0] : 20010115
        for t in tagd.items: # ex) t[0] : duplicate
            for data in t[1].items(): # ex) data[0] : peer1
                pddata[t[0]] = concat(pddata, pd.DataFrame(data.values()), axis=0)

    print pddata

    for tagd in sorted(tags.items(), key = lambda x: x[0]):
        for item in tagd[1].items():
            if item[0] not in tag:
                tag[item[0]] = list()
            tag[item[0]].append(item[1])
    # correlation coefficient
    for t in tag.items():
        sys.stdout.write(t[0] + " ")
    print(" ")
    for t in tag.items():
        for s in tag.items():
            sys.stdout.write(str(np.corrcoef(t[1], s[1])[0,1]) + " ")
        sys.stdout.write("\n")

    for t in tag.items():
        ones = np.ones(6)/6
        x = sorted(tags.keys())
        y = np.convolve(t[1], ones, "valid").tolist()
        for i in range(0, (len(t[1])-len(y))/2):
            x.pop(0)
            x.pop(-1)
        x.pop(0)
        print len(x)
        print len(y)
        #print t
        #print t[1]
        ax.plot(x, y, label = t[0])

        #ax.plot(np.array([1,2,3,4,5]), t[1])
    #ax.get_xaxis().get_major_formatter().set_useOffset(False)
    #ax.get_xaxis().set_major_locator(ticker.MaxNLocator(integer=True))
    lgnd = plt.legend(bbox_to_anchor=(1.05, 0), loc='lower left', borderaxespad=0)
    #ax.set_title(' test ')
    months = mdates.YearLocator()
    daysFmt = mdates.DateFormatter("%Y")
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(daysFmt)
    #ax.set_yscale("log")
    
    ax.set_xlabel("year")
    ax.set_ylabel("the number of tag")
    plt.savefig( "../../Data/graphs/test",bbox_extra_artists=(lgnd,), bbox_inches='tight')

tags = dict()
pkl = args.pickle_file
with open(pkl, "rb") as f:
    tag_data = pickle.load(f)
    for tag_year in sorted(tag_data.items(), key = lambda x: x[0]):
        #if tag_year[0][:4] == "2016":
           # continue
        tags[dt.strptime(tag_year[0], "%Y%m%d")] = tag_year[1]

save_figure(tags)
