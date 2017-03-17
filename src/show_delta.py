import numpy as np
import sys
import matplotlib
matplotlib.use("AGG")
from matplotlib import pyplot as plt


f = open(sys.argv[1] , "r")
tag = {}


for line in f:
    if "debug" not in line:
        continue

    res = line.split(":")
    #['debug ', 'all ', '  0 4.6e-05\n']
    i, time = res[2].split()
    res[1].split()
    if res[1] not in tag:
        tag[res[1]] = []
        tag[res[1]].append([])
        tag[res[1]].append([])
    tag[res[1]][0].append(i)
    tag[res[1]][1].append(time)

    #['radix_update', ':', '3688', '2e-06'] 
    #['term1 ', 'Update_header ', 'community, attribute, duplicate ', 'radix_update ', 'prepending ', 'footer ', 'Update ', 'origin, path, community, attribute ', 'newprefix ', 'Withdraw ', '\n'] 
print tag.keys()
fig = plt.figure()
for t in tag.items():
    ax = fig.add_subplot(1,1,1)
    ax.scatter(t[1][0],t[1][1])
    ax.set_xlabel("message")
    ax.set_ylabel("time(s)")
#ax.set_xscale("log")
ax.set_title("term speed of blt")
plt.savefig("/home/tktbtk/Data/delta.png")
    
     
