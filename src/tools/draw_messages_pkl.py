import glob
import argparse
import sys
import pickle
import csv
import matplotlib
matplotlib.use("AGG")
from matplotlib import pyplot as plt
from datetime import datetime as dt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates


parser = argparse.ArgumentParser()
parser.add_argument("blt_file", help = "import blt file", nargs = "*")
parser.add_argument("outfile", help="output file")

args = parser.parse_args()


if args.blt_file is None:
    sys.stderr.write("There is no blt_file. Please input it")
    sys.exit()

y = list()
x = list()
#print "date messages duplicate_announce new_prefix attribute_change path_change community_change duplicate_withdraw prepending origin_change remove_prefix"
for blt_file in args.blt_file:
    date = blt_file.split("/")[-1].split(".")[0]
    if "_" in date:
        date = date.split("_")[0]
    print "reading " + date + " now"
#20140715.blt
    date = dt.strptime(date, "%Y%m%d")
    blt_files = glob.glob(blt_file)
    
    if len(blt_files)==0:
        sys.exit()
                    
    blt_files.sort()
    messages = 0


    for bf in blt_files:
        blt = open(bf, "r")
        for line in blt:
            messages += 1
    x.append(date)
    y.append(messages)
    print y
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(x,y)
g = open("test.pkl", "wb")
pickle.dump([x,y], g)
plt.rcParams["font.size"] = 18
months = mdates.YearLocator()
daysFmt = mdates.DateFormatter("%Y")
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(daysFmt)
#ax.set_yscale("log")
ax.set_ylabel("the number of BGP-messages")
ax.set_xlabel("year")
plt.savefig("test")
