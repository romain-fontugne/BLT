import sys
from subprocess import Popen, PIPE
import glob
import radix
import hashlib
from collections import deque

def readrib(files):
    
    rtreedict = {}
    queues = {}
    sflags = {}

    p1 = Popen(["bgpdump", "-m", "-v", "-t", "change", files], stdout=PIPE, bufsize=-1)

    for line in p1.stdout: 
        res = line.split('|',15)
        zTd, zDt, zS, zOrig, zAS, zPfx, sPath, zPro, zOr, z0, z1, z2, z3, z4, z5 = res
        
        if zPfx == "0.0.0.0/0":
	    print line
            continue

        if rtreedict.has_key(zOrig) is False:
            rtreedict[zOrig] = radix.Radix()
            queues[zOrig] = deque()
            sflags[zOrig] = {}
            sflags[zOrig]["before"] = 0
            sflags[zOrig]["now"] = 0

        node = rtreedict[zOrig].add(zPfx)
        node.data["firsttime"] = zDt
        node.data["lasttime"] = zDt
        node.data["path"] = sPath 
        node.data["community"] = z2
        node.data["MD5"] = hashlib.md5(z0 + z1 + z2 + z3 + z4 + z5).digest()
        node.data["as"] = sPath.split(" ")[-1]

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
    return_list = [rtreedict, queues, sflags]
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
    rtreedict = readrib(files[0])
    #for zOrig, rtree in rtreedict.items():
    #    for rnode in rtree:
    #        print("%s %s: #%s   top_prefix = %s" % (zOrig, rnode.prefix, rnode.data["prefix_category"], rnode.data["top_prefix"]))

