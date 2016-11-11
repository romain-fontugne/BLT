import sys
import pickle
import matplotlib.pyplot as plt
import numpy as np

args = sys.argv
with open(args[1], mode="rb") as f:
    pfx_data = pickle.load(f)

f.close

path_change = sorted(pfx_data.items(), key=lambda x: x[1]["path_change"])

x=[]
y=[]

for n in path_change:
    x.append(n[1]["path_change"])
    y.append(n[1]["message"])

plt.scatter(x,y)
#ax = plt.gca()
#ax.invert_xaxis()
plt.xlim([200,0])
plt.ylim([0,600])
plt.ylabel("#messages")
plt.xlabel("#path_change")

plt.show()
