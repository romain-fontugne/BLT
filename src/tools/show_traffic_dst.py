import numpy as np
import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt

y = {}

f = open("bytesPerDst.txt", "r")
i=0
for line in f:
	if line.find("!") >= 0:
		continue
	line = line.translate(None,"\n").split(" ")
	label = line[0]
	value = int(line[1])
	if value in y:
		y[value] += 1
	else:
		y[value] = 1
for data in y.items():
	if data[1] <10:
		y.pop(data[0])
	else:
		print data
	

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.scatter(y.keys(), y.values())

ax.set_title('traffic volume vs #dst')
ax.set_xlabel('traffic volume')
ax.set_ylabel('#dst')

plt.savefig( 'test.png' )
