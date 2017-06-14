import matplotlib
import allrolling_std
import sys
matplotlib.use("AGG")
from matplotlib import pyplot as plt
import numpy as np
import argparse
import pickle
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from datetime import datetime as dt
import pandas as pd
#from allrolling_std import *


parser = argparse.ArgumentParser()
parser.add_argument("pickle_file")
parser.add_argument("-d", "--median", help = "output granph which use median values of each peer.", action = "store_true")
parser.add_argument("-m", "--mean", help = "output granph which use mean values of each peer.", action = "store_true")
parser.add_argument("-t", "--tag_name", help = "output granph which use values of each peer separately.")
parser.add_argument("-s", "--std", help = "You can output tagtime graph with standard diviation", action = "store_true")
parser.add_argument("-r", "--threshold")
args = parser.parse_args()


kinds_tag = ["path_change", "remove_prefix", "attribute_change", "new_prefix", "community_change", "other_change", "path_switching", "prepending_add", "prepending_change", "prepending_remove", "origin_change", "duplicate_withdraw", "duplicate_announce", "messages"]

if args.median == True and args.mean == False and args.tag_name == None:
    way = "median"
elif args.median == False and args.mean == True and args.tag_name == None:
    way = "mean"
elif args.median == False and args.mean == False and args.tag_name != None:
    if args.std == False:
        way = "tag_name"
    else:
        way = "tag_name_std"
    if args.tag_name not in kinds_tag:
        print "please input correct tag_name. exit"
        sys.exit()
else:
    print "please select one option. -s or -m or -d"
    sys.exit()
def save_figure(tags, output):
        # tags                  = { time : { tag : { peer : data }}}
        # tagd                  = ( time, { tag : { peer : data }})
        # t                     = ( tag , { peer : data })
        # d                     = ( peer, data)
        # data (tag_name)       = { tag : { peer : [data] }}
        # data (mean, median)   = { tag : [data]}
        # peerlist              = [peers ]
        # remove_peer           = [peers]
 
    tag = dict()
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    pddata = dict()
    data = dict()
    x = list()
    results = dict()
    peerlist = list()
    remove_peer = list()
    for kt in kinds_tag:
        data[kt] = dict()
    # time 
    for tagd in sorted(tags.items(), key = lambda x: x[0]): # ex) tagd[0] : 20010115
        x.append(tagd[0])
        
        for message_peer in tagd[1]["messages"].keys():
            if message_peer not in peerlist:
                peerlist.append(message_peer)
                if message_peer in remove_peer:
                    remove_peer.remove(message_peer)
                if message_peer not in data["messages"].keys():
                    for kt in kinds_tag:
                        data[kt][message_peer] = ["-"]*(len(x)-1)

        for exist_peer in peerlist:
            if exist_peer not in tagd[1]["messages"].keys():
                remove_peer.append(exist_peer)
                peerlist.remove(exist_peer)
        
        for kt in kinds_tag:
            for rp in remove_peer:
                data[kt][rp].append("-")
            if kt not in tagd[1].keys():
                for p in peerlist:
                    data[kt][p].append(0)
        
        for t in tagd[1].items(): # t = (tag, {peer: data})
            for p in peerlist:
                if p not in t[1].keys():
                    data[t[0]][p].append(0)
            for d in t[1].items(): # ex) d = (peer, data)
                data[t[0]][d[0]].append(d[1])

    if way == "tag_name":
        y = dict()
        for peer in data[args.tag_name].items(): # peer = (peer : data)
            for i in range(len(peer[1])):
                if peer[1][i] == "-":
                    data[args.tag_name][peer[0]][i] = 0
        for peer in data[args.tag_name].items():
            if max(peer[1]) < int(args.threshold):
                continue     
            ones = np.ones(6)/6
            y[peer[0]] = np.convolve(peer[1], ones, "same").tolist()
            ax.plot(x, y[peer[0]], label = peer[0])
            if sum(y[peer[0]])/len(y[peer[0]]) < 1:
                y_axis = "the ratio of " + args.tag_name
            else:
                y_axis = "the number of " + args.tag_name
        ax.set_ylabel(y_axis)
        ax.set_title(y_axis)
        lgnd = plt.legend(bbox_to_anchor=(1.05, 0), loc='lower left', borderaxespad=0)
        output = output + "_" + args.tag_name + "_thr.png"

    else:
        for d in data.items():
            ta = ""
            if d[0] == "prepending_remove":
                ta = "PrR"
            elif d[0] == "prepending_add":
                ta = "PrA"
            elif d[0] == "prepending_change":
                ta = "PrC"
            else:
                for t in d[0].split("_"):
                    ta += t[0].upper()
            mean, median, std = allrolling_std.allrolling_std(data[d[0]].values(), 6)
            results[ta] = dict()
            results[ta]["mean"] = mean
            results[ta]["median"] = median
            results[ta]["std"] = std
        x.pop(0)
        x.pop(0)
        x.pop(0)
        x.pop(-1)
        x.pop(-1)
        if sum(results["DA"]["mean"])/len(results["DA"]["mean"]) < 1:
            if way == "mean" or way == "median":
                y_axis = "the ratio of each tag"
            else:
                y_axis = "the ratio of " + args.tag_name
        else:
            if way == "mean" or way == "median":
                y_axis = "the number of each tag"
            else:
                y_axis = "the number of " + args.tag_name
        

        if way == "mean" or way == "median":
            for result in results.items():
                if result[0] == "M":
                    continue
                if way == "mean":
                    ax.plot(x,result[1]["mean"], label = result[0])
                if way == "median":
                    ax.plot(x,result[1]["median"], label = result[0])
            lgnd = plt.legend(bbox_to_anchor=(1.05, 0), loc='lower left', borderaxespad=0)
            ax.set_title(y_axis + "(" + way + ")")
            ax.set_ylabel(y_axis)
        elif way == "tag_name_std":
            ax.plot(x,results[args.tag_name]["mean"])
            ax.set_ylabel(y_axis)
            ax.set_title(y_axis + " and standard diviation")
            ax.errorbar(x, results[args.tag_name]["mean"], yerr=std)
            output = output + "_" + args.tag_name + "_std.png"
        
            



    #ax.set_title(' test ')
    plt.rcParams["font.size"] = 18
    daysFmt = mdates.DateFormatter("%Y")
    ax.xaxis.set_major_formatter(daysFmt)
    #ax.set_yscale("log")
    ax.set_xlabel("year")
    #plt.savefig( "../../../Data/graphs/test",bbox_extra_artists=(lgnd,), bbox_inches='tight')
    if way == "tag_name_std" or way == "tag_name":
        plt.savefig(output,bbox_extra_artists=(lgnd,), bbox_inches='tight')
    else:
        if way == "mean":
            output += "_mean.png"
        elif way == "median":
            output += "_median.png"
        plt.savefig(output ,bbox_extra_artists=(lgnd,), bbox_inches='tight')

    # bad boy
    #badboy = list()
    #for peer in data["duplicate_announce"].items():
    #    for d in peer[1]:
    #        if float(d) > 0.9:
    #            if peer[0] not in badboy:
    #                badboy.append(peer[0])

   # correlation coefficient
#    for t in tag.items():
#        sys.stdout.write(t[0] + " ")
#    print(" ")
#    for t in tag.items():
#        for s in tag.items():
#            sys.stdout.write(str(np.corrcoef(t[1], s[1])[0,1]) + " ")
#        sys.stdout.write("\n")
#    dups = data["duplicate_announce"].values()
    # dups = [[1,2,3,4,5], [2,3,4,5,6],,,,]
#    y = list()
#    test = list()
#    for t in range(len(x)):
#        p = list()
#        for dup in dups:
#            p.append(dup[t])
#        y.append(np.median(p))
#        test.append(sorted(p))
    #for t in test:
    #    for tt in t:
        #    sys.stdout.write(str(tt) + ", ")
        #sys.stdout.write("\n")
#    ax.plot(x, y)     
        

        #ax.plot(np.array([1,2,3,4,5]), t[1])

tags = dict()
pkl = args.pickle_file
with open(pkl, "rb") as f:
    tag_data = pickle.load(f)
    for tag_year in sorted(tag_data.items(), key = lambda x: x[0]):
        #if tag_year[0][:4] == "2016":
           # continue
        tags[dt.strptime(tag_year[0], "%Y%m%d")] = tag_year[1]
file_name = pkl.split("/")[-1].split(".")[0]
output = "/home/tktbtk/Data/graphs/paper_"+file_name
save_figure(tags, output)
