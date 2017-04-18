import sys
from subprocess import Popen, PIPE
import glob
import radix
import hashlib
from collections import deque

def readrib(files):
    
    peers = dict()
    rtree = radix.Radix()

    p1 = Popen(["bgpdump", "-m", "-v", "-t", "change", files], stdout=PIPE, bufsize=-1)

    for line in p1.stdout: 
        res = line.split('|',15)
        zTd, zDt, zS, zOrig, zAS, zPfx, sPath, zPro, zOr, z0, z1, z2, z3, z4, z5 = res
        
        if zPfx == "0.0.0.0/0":
            continue

        if peers.has_key(zOrig) is False:
            peers[zOrig] = dict()
            peers[zOrig]["queues"] = deque()
            peers[zOrig]["sflags"] = dict()
            peers[zOrig]["sflags"]["before"] = 0
            peers[zOrig]["sflags"]["now"] = 0

        node = rtree.add(zPfx)
        if zOrig not in node.data:
            node.data[zOrig] = dict()
        node.data[zOrig]["firsttime"] = zDt
        node.data[zOrig]["lasttime"] = zDt
        node.data[zOrig]["path"] = sPath 
        node.data[zOrig]["community"] = z2
        node.data[zOrig]["MD5"] = hashlib.md5(z0 + z1 + z2 + z3 + z4 + z5).digest()
        node.data[zOrig]["as"] = sPath.split(" ")[-1]
        

    # Detect category of each prefix
#    for rtree in rtreedict.values():
#        for node in rtree:
#            top = rtree.search_worst(node.prefix)
#            node.data["top_prefix"] = top.prefix
#            if top.prefix == node.prefix:
#                if len(rtree.search_covered(node.prefix)) == 1:
#                    node.data["prefix_category"] = "lonely"
#                else:
#                    node.data["prefix_category"] = "top"
#            else:
#                if top.data["as"] == node.data["as"]:
#                    node.data["prefix_category"] = "delegated"
#                else:
#                    node.data["prefix_category"] = "deaggregated"
    print "The number of peers is " + str(len(peers))
    return_list = [rtree, peers]
    return return_list

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("usage: %s ribfiles*.bz2" % sys.argv[0])
        sys.exit()
        
    # list rib files
    files = glob.glob(sys.argv[1])
    if len(files)==0:
        print("Files not found!")
        sys.exit()

    files.sort()
    rtree = readrib(files[0])
