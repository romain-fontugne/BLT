import matplotlib
matplotlib.use("AGG")
from matplotlib import pyplot as plt
import numpy as np
import sys
import pickle
from datetime import datetime as dt


with open(sys.argv[1], "rb") as f:
    tags = pickle.load(f)

sdate = 20150101
fdate = 20160101
tagging = dict()
for month, tag in tags.items():
    if sdate < int(month) < fdate:
        for t in tag.items():
            if t[0] not in tagging:
                tagging[t[0]] = 0
            tagging[t[0]] += t[1]

data = list()
label = list()
for t in tagging.items():
    data.append(t[1])
    label.append(t[0])

print data
print label
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.pie(data, labels = label)
plt.savefig( "../../Data/graphs/test")
