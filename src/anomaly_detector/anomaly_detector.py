import matplotlib
matplotlib.use("AGG")
from matplotlib import pyplot as plt
import numpy as np
import argparse
import pickle
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from matplotlib import gridspec
from datetime import datetime as dt
from datetime import timedelta as td

def mad(arr):
    arr = np.ma.array(arr).compressed() # should be faster to not use masked arrays.
    med = np.median(arr)
    return np.median(np.abs(arr - med))

def __roleFormatter(x, pos):
    res = ""
    for at in alert_tags.items():
        if x == at[1]:
            res = at[0]
    return res

##### set variables #####
movingValue = 30
ones = np.ones(movingValue)/movingValue
maximumY = 0
maximumY2 = 0

##### arguments #####
parser = argparse.ArgumentParser()
parser.add_argument("pickle_file")
parser.add_argument("-t", "--tags", help = "if you want to draw only several tags. ex) duplicate_announce,new_prefix")
parser.add_argument("-l", "--log", help = "if you want to draw as log scale.", action = "store_true")
parser.add_argument("-i", "--incident", help = "route_leak or hijack")
parser.add_argument("-b", "--bean", default=10)
args = parser.parse_args()
outfile = args.pickle_file.split(".")[0]

if args.incident == "route_leak":
    ### route leak ###
    print "Route Leak!"
    other_tags = ["prepending_add", "prepending_change", "prepending_remove", "path_switching", "other_change", "duplicate_withdrawal", "origin_change"]
    alert_tags = dict()
    alert_tags["duplicate_announce"] = 0
    alert_tags["community_change"] = 1
    alert_tags["transit_change"] = 2
    alert_tags["new_prefix"] = 3
    alert_tags["remove_prefix"] = 4

elif args.incident == "hijack":
    ### highjack ###
    print "Hijack!"
    other_tags = ["prepending_add", "prepending_change", "prepending_remove", "path_switching", "other_change", "duplicate_withdrawal"] 
    alert_tags = dict()
    alert_tags["other_change"] = 0
    alert_tags["duplicate_announce"] = 1
    alert_tags["remove_prefix"] = 2
    alert_tags["origin_change"] = 3
    alert_tags["new_prefix"] = 4
elif args.incident == "outage":
    print "Outage!"
    other_tags = ["prepending_add", "prepending_change", "prepending_remove", "path_switching", "other_change", "duplicate_withdrawal"] 
    alert_tags = dict()
    alert_tags["duplicate_announce"] = 0
    alert_tags["community_change"] = 1
    alert_tags["remove_prefix"] = 2
    alert_tags["transit_change"] = 3
    alert_tags["new_prefix"] = 4

else:
  other_tags = []
  alert_tags = dict()
  alert_tags["duplicate_announce"] = 0
  alert_tags["duplicate_withdrawal"] = 1
  alert_tags["community_change"] = 2 
  alert_tags["remove_prefix"] = 3
  alert_tags["transit_change"] = 4
  alert_tags["origin_change"] = 5
  alert_tags["new_prefix"] = 6


##### get date #####
date = args.pickle_file.split("/")[-1][:8]
startTime = dt.strptime(date + "0000", "%Y%m%d%H%M")
endTime = dt.strptime(date + "2359", "%Y%m%d%H%M")

##### pickle load #####
pkl = args.pickle_file
with open(pkl, "rb") as f:
    data = pickle.load(f)   ## data[tagName][time] = [value]
alert_flags = dict()
window_data = dict()
sorted_data = dict()
for tag in data.items():
    timeStamp = startTime
    window_data[tag[0]] = dict()
    window_data[tag[0]][timeStamp] = 0
    for t in sorted(tag[1].items(), key=lambda x:x[0]):
        if t[0] >= timeStamp + td(minutes=args.bean):
          timeStamp += td(minutes=args.bean)
        if timeStamp not in window_data[tag[0]].keys():
          window_data[tag[0]][timeStamp] = 0
        window_data[tag[0]][timeStamp] += t[1]
    #sorted_data[tag[0]] = np.array(sorted(tag[1].items(), key=lambda x: x[0]))[:,1]
    sorted_data[tag[0]] = np.array(sorted(window_data[tag[0]].items(), key=lambda x: x[0]))[:,1]
    alert_flags[tag[0]] = 0

data = window_data

info = dict()
print "####################################"
print "tag_name : [median, std, threashold]"
print ""
for sdata in sorted_data.items():
    # info = {tag_name : [median, std, threshold]
    ndata = np.array(sdata[1])
    info[sdata[0]] = list()
    if len(ndata[ndata!=0]) == 0:
      info[sdata[0]].append(True)
      info[sdata[0]].append(True)
      info[sdata[0]].append(True)
      print "There is no messages clasyfied as " + sdata[0]
    else:
      #info[sdata[0]].append(np.median(sdata[1]))
      #info[sdata[0]].append(mad(sdata[1]))
      #info[sdata[0]].append(info[sdata[0]][0] + info[sdata[0]][1] * 10)
      info[sdata[0]].append(np.median(ndata[ndata!=0]))
      info[sdata[0]].append(mad(ndata[ndata!=0]))
      info[sdata[0]].append(info[sdata[0]][0] + info[sdata[0]][1] * 10)
      print sdata[0] + ": " + str(info[sdata[0]])
print "####################################"
print ""

##### figure format #####
fig = plt.figure()
gs = gridspec.GridSpec(3,1, height_ratios=[2,4,2])
scatter = False
daysFmt = mdates.DateFormatter("%H")

ax1 = fig.add_subplot(gs[0])
ax1.set_xticklabels([])
ax1.set_ylabel("# update messages")
ax1.grid(True)
ax2 = fig.add_subplot(gs[1])
ax2.set_xticklabels([])
ax2.set_ylabel("# labels")
ax2.grid(True)
ax3 = fig.add_subplot(gs[2])
ax3.xaxis.set_major_formatter(daysFmt)
ax3.set_xlabel("hour")
ax3.grid(True)

##### plot total number of messages #####
tag_array = list()
tag_array_raw = list()
for tag in data.items():
    timeStamp = startTime
    x = list()
    y = list()

    for item in sorted(tag[1].items(), key=lambda x: x[0]):
        while timeStamp < item[0]:
            x.append(timeStamp)
            y.append(0)
            timeStamp += td(minutes=args.bean)
        x.append(timeStamp)
        y.append(item[1])
        timeStamp += td(minutes=args.bean)
    while endTime >= timeStamp:
      x.append(timeStamp)
      y.append(0)
      timeStamp += td(minutes=args.bean)
    tag_array_raw.append(y)
    y = np.convolve(y, ones, "same").tolist()
    tag_array.append(y)
tag_np_array = np.array(tag_array)

total_messages = np.sum(tag_np_array, axis=0)
total_messages_raw = np.sum(np.array(tag_array_raw), axis=0)

ax1.plot(x, total_messages_raw)

##### other data #####
other_data = dict()
for tag in data.items():
    timeStamp = startTime
    if tag[0] not in other_tags:
        continue
    for item in sorted(tag[1].items(), key=lambda x: x[0]):
        while  timeStamp < item[0]:
            if timeStamp not in other_data.keys():
                other_data[timeStamp] = 0
            timeStamp += td(minutes=args.bean)
        if timeStamp == item[0]:
            if timeStamp not in other_data.keys():
                other_data[timeStamp] = item[1]
            else:
                other_data[timeStamp] += item[1]
            timeStamp += td(minutes=args.bean)
        else:
            print "ERROR!!!"
            print "timestamp: " + str(timeStamp)
            print "data TS  : " + str(item[0])
            break

tagColors = ['blue', 'turquoise', 'g','greenyellow', 'y', 'gold', 'coral', 'r', 'mediumvioletred', 'purple','indigo', 'rosybrown', 'cadetblue','k']
for (tag,C) in zip(data.items(), tagColors):
    timeStamp = startTime
    if tag[0] in other_tags:
        continue
    x = list()
    y = list()
    alert = list()

    ##### timestamp processing #####
        # if the starttime is lower than the timestamp of the message, append 0 to y #
    while timeStamp < sorted(tag[1].keys())[0]:
        x.append(timeStamp)
        y.append(0)
        timeStamp += td(minutes=args.bean)

    ##### append the number of updates #####
    for item in sorted(tag[1].items(), key=lambda x: x[0]):
        while timeStamp < item[0]:
            x.append(timeStamp)
            y.append(0)
            timeStamp += td(minutes=args.bean)
        y.append(item[1])
        x.append(item[0])
        timeStamp += td(minutes=args.bean)

    while endTime >= timeStamp:
      x.append(timeStamp)
      y.append(0)
      timeStamp += td(minutes=args.bean)

    ##### moving average #####
    if len(y) >= movingValue:
        y2 = np.convolve(y, ones, "same").tolist()
    else:
        y2 = y

    ### not moving value
    y2 = y

    ##### max value, min value #####
    if max(y) > maximumY:
        maximumY = max(y)
    if max(y2) > maximumY2:
        maximumY2 = max(y2)

    ##### plot tags figure #####
    lgnd = ax2.legend(bbox_to_anchor=(1.05, 0), loc='lower left', borderaxespad=0)
    if args.log == True:
        ax2.set_yscale("log")
        outfile = outfile + "_log"
    if scatter == True:
        ax2.scatter(x,y, s=20, c=C, marker='+', label=tag[0])
        ax2.plot(x,y2,c=C, alpha=0.3 ,linewidth=1)
    else:
        ax2.plot(x,y2,c=C, linewidth=1, label = tag[0])

    ##### alert ######
    for (ts, value) in zip(x, y2):
        if alert_flags[tag[0]] == 0:
            if value > info[tag[0]][2]:
                print "alert! " + str(ts) + " " + tag[0] + " value: " + str(value) + " thr:" + str(info[tag[0]][2])
                for i in range(args.bean):
                    alert.append(ts)
                    ts += td(minutes=1)
                alert_flags[tag[0]] = 1
        else:
            if value <= info[tag[0]][2]:
                print "fixed! " + str(ts) + " " + tag[0]
                alert_flags[tag[0]] = 0
            else:
                for i in range(args.bean):
                    alert.append(ts)
                    ts += td(minutes=1)

    if len(alert) >= 1:
        if tag[0] in alert_tags.keys():
            alert_value = [alert_tags[tag[0]]] * len(alert)
            ax3.plot(alert, alert_value, "+" , c="r")
            

        
##### plot other tag #####
x = list()
y = list()
for data in sorted(other_data.items(), key=lambda x : x[0]):
    x.append(data[0])
    y.append(data[1])
    
if len(y) != 0:
  #y2 = np.convolve(y, ones, "same").tolist()
  y2 = y
  if args.log == True:
      ax2.set_yscale("log")
  if scatter == True:
      ax2.scatter(x,y2, s=20, c=C, marker='+', label= "other change")
      ax2.plot(x,y2,c="k", alpha=0.3 ,linewidth=1)
  else:
      ax2.plot(x,y2,c="k", linewidth=1, label = "other change")
lgnd = ax2.legend(bbox_to_anchor=(0.35, -0.87),ncol=3, loc='upper center', borderaxespad=0)
##### plot other tag #####
if max(y2) > maximumY2:
   maximumY2 = max(y2)

ax3.set_xlim(startTime, endTime)
ax3.set_ylim(-0.5, len(alert_tags) - 0.5)
ax3.yaxis.set_major_formatter(ticker.FuncFormatter(__roleFormatter))
if args.log == True:
    ax2.set_ylim(1, (maximumY*20/10))
else:
    ax2.set_ylim(0, (maximumY2*11/10))
plt.grid(which="major", color="black", linestyle="dotted")

outfile = outfile + ".eps"
plt.savefig(outfile, bbox_extra_artists=(lgnd,), bbox_inches='tight')
