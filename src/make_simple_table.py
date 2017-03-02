import argparse
import sys
import pickle
import csv


parser = argparse.ArgumentParser()
parser.add_argument("-b", "--blt_file", help = "import blt file")
parser.add_argument("-p", "--peers", help = "number of peers")

args = parser.parse_args()

pfx_data = {}
tags = dict()
default_route = 0

if args.blt_file is None:
    sys.stderr.write("There is no blt_file. Please input it")
    sys.exit()

blt = open(args.blt_file, "r")
for line in blt:
    tag = line.split("\n")[0].split(" #")[1]
    if tag not in tags:
        tags[tag] = 0
    else:
        tags[tag] += 1

for tag in tags.items():
    tags[tag[0]] = tag[1] / int(args.peers)
print ' '.join(tags.keys())
print ' '.join(map(str,tags.values()))
pkl_file = "/home/tktbtk/Data/pickel/" + args.blt_file.split(".")[0] + ".pkl"
with open(pkl_file, mode = "wb") as f:
    pickle.dump(tags, f)
