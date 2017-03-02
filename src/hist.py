import argparse
import sys

withd = 0
dup_withd = 0

blt_file = open(sys.argv[1], "r")
for line in blt_file:
    res = line.split("|")
    zS = res[2]
    if zS == "A":
        sPath = res[6]
        print sPath
