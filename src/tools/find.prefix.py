import matplotlib
matplotlib.use("AGG")
from matplotlib import pyplot as plt
import datetime
import argparse
import sys
import glob
import matplotlib.ticker as ticker
import matplotlib.dates as mdates

parser = argparse.ArgumentParser()
parser.add_argument("blts", nargs = "*")

args = parser.parse_args()


pfx = list()
number = 0
dates = list()
prefixes = dict()

for blt in args.blts:
    print >> sys.stderr, "reading %s now..." % blt
    
    #20130615.blt
    date = blt.split("/")[-1][0:8]
    dates.append(date)

    blt_files = glob.glob(blt)
    
    if len(blt_files)==0:
        sys.exit()
                    
    blt_files.sort()
    day_prefixes =dict()
    for p in pfx:
        day_prefixes[p] = 0
    for bf_ in blt_files:
        bf = open(bf_, "r")
        for line in bf:
            if "duplicate_announce" not in line:
                continue
            res = line.split("#")[0].split("|")
            zTd, zDt, zS, zOrig, zAS, zPfx, sPath, zPro, zOr, z0, z1, z2, z3, z4, z5 = res
            if zPfx not in pfx:
                pfx.append(zPfx)
                day_prefixes[zPfx] = 0
                prefixes[zPfx] = [0]*number
            day_prefixes[zPfx] += 1
    print day_prefixes
    for prefix in day_prefixes.items():
        prefixes[prefix[0]].append(day_prefixes[1])
    number += 1
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
for prefix in prefixes.items():
    print prefix[0]
    ax.plot(dates, prefix[1], label=prefix[0])

lgnd = plt.legend(bbox_to_anchor=(1.05, 0), loc='lower left', borderaxespad=0)
months = mdates.YearLocator()
daysFmt = mdates.DateFormatter("%Y-%m")
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(daysFmt)
plt.savefig("test")
