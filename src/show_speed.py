import numpy as np
import matplotlib
matplotlib.use("AGG")
from matplotlib import pyplot as plt
import sys

x = list()
y = list()
time = list()

try:
    f = open(sys.argv[1] , "r")
except:
    print "There is no argument. Exit"
    exit(0)
i = 1
for line in f:
    line = line.split("\n")[0]
    if "reading" in line:
        continue
    if line not in time:
        time.append(line)
        y.append(0)
        x.append(i)
        i += 1
    y[len(x)-1] += 1

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(x,y)
ax.set_title("blt.py speed")
ax.set_xlabel("time (s)")
ax.set_ylabel("the number of messages")
#ax.set_xscale("log")
ax.set_yscale("log")
plt.savefig("/home/tktbtk/Data/" + sys.argv[1].split("/")[-1] + ".png")
print x
print y
