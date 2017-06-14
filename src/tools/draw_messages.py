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




f = open("test.pkl", "rb")
x, y = pickle.load(f)
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(x,y)
plt.rcParams["font.size"] = 18
daysFmt = mdates.DateFormatter("%Y")
ax.xaxis.set_major_formatter(daysFmt)
#ax.set_yscale("log")
ax.set_ylabel("the number of BGP-messages")
ax.set_xlabel("year")
plt.savefig("test")
