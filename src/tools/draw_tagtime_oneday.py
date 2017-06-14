import matplotlib
import sys
matplotlib.use("AGG")
from matplotlib import pyplot as plt
import numpy as np
import argparse
import pickle
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from datetime import datetime as dt


parser = argparse.ArgumentParser()
parser.add_argument("pickle_file")
parser.add_argument("outfile")
parser.add_argument("-t", "--tags", help = "if you want to draw only several tags. ex) duplicate_announce,new_prefix")
args = parser.parse_args()

def save_figure(tags, outfile, tag_flag):
    # tags = {time : {tag_name : value}} 
    tag = dict()
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    tag_name = ["duplicate_announce", "new_prefix", "attribute_change", "path_change", "community_change", "duplicate_withdraw", "prepending", "origin_change", "remove_prefix"]
    for tagd in sorted(tags.items(), key = lambda x: x[0]): # tagd = (time, {tag_name : value})
        for item in tagd[1].items(): # item = (tag_name, value)
            if item[0] not in tag:
                tag[item[0]] = list()
            tag[item[0]].append(item[1]) # tag = {tag_name : [value, value,,,]}

    if tag_flag != None:
        tag_name = args.tags.split(",")
    # correlation coefficient
    for t in tag.items():
    #    sys.stdout.write(t[0] + " ")
        pass
    #print(" ")
    for t in tag.items():
        for s in tag.items():
            pass
     #       sys.stdout.write(str(np.corrcoef(t[1], s[1])[0,1]) + " ")
     #   sys.stdout.write("\n")

    for t in tag.items():
        ones = np.ones(30)/30
        x = sorted(tags.keys())
        y = np.convolve(t[1], ones, "same").tolist()
        ax.plot(x, y, label = t[0])
        #print t
        #print t[1]

        #ax.plot(np.array([1,2,3,4,5]), t[1])
    #ax.get_xaxis().get_major_formatter().set_useOffset(False)
    #ax.get_xaxis().set_major_locator(ticker.MaxNLocator(integer=True))
    #ax.set_title(' test ')
    #months = mdates.YearLocator()
    daysFmt = mdates.DateFormatter("%H")
    #ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(daysFmt)
    #ax.set_yscale("log")
    print x
    
    ax.set_xlabel("hour")
    ax.set_ylabel("the number of tag")
    if len(tag_name) != 1:
        lgnd = plt.legend(bbox_to_anchor=(1.05, 0), loc='lower left', borderaxespad=0)
        ax.plot(x, y, label = tag_name)
        plt.savefig(outfile ,bbox_extra_artists=(lgnd,), bbox_inches='tight')
    else:
        plt.savefig(outfile)

tags = dict()
pkl = args.pickle_file
with open(pkl, "rb") as f:
    tag_data = pickle.load(f)
    for tag_year in sorted(tag_data.items(), key = lambda x: x[0]):
        #if tag_year[0][:4] == "2016":
           # continue
        tags[tag_year[0]] = tag_year[1]

save_figure(tags, args.outfile, args.tags)
