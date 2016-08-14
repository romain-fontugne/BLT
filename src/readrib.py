import sys
from subprocess import Popen, PIPE
import glob
import radix
import hashlib

def readrib(files):
    
    peertree=radix.Radix()
    rtreelist = [peertree]
    p0 = Popen(["bzcat"]+files, stdout=PIPE, bufsize=-1)
    p1 = Popen(["bgpdump", "-m", "-v", "-t", "change", "-"], stdin=p0.stdout, stdout=PIPE, bufsize=-1)

    for line in p1.stdout: 
        res = line.split('|',15)
        zTd, zDt, zS, zOrig, zAS, zPfx, sPath, zPro, zOr, z0, z1, z2, z3, z4, z5 = res
        prefix = "".join(zOrig.split("."))
        prefix = "".join(prefix.split(":"))

        if peertree.search_exact(zOrig) is None:
            peertree.add(zOrig)
            exec("rtree_" + prefix + "=radix.Radix()")
            exec("rtreelist.append(rtree_" + prefix + ")")
        exec("node = rtree_" + prefix + ".add(zPfx)")
        node.data["firsttime"] = zDt
        node.data["lasttime"] = zDt
        node.data["path"] = sPath 
        node.data["community"] = z2
        node.data["peer"] = zOrig
        node.data["MD5"] = hashlib.md5(z0 + z1 + z2 + z3 + z4 + z5).digest()
        node.data["as"] = sPath.split(" ")[-1]
    
    # Detect status of each prefix
    for rtree in rtreelist[1:]:
        for node in rtree:
            if rtree.search_worst(node.prefix).prefix == node.prefix:
                if len(rtree.search_covered(node.prefix)) == 1:
                    node.data["status"] = "lonely"
                else:
                    node.data["status"] = "top"
            else:
                if rtree.search_worst(node.prefix).data["as"] == node.data["as"]:
                    node.data["status"] = "delegated"
                else:
                    node.data["status"] = "deaggregated"

    return rtreelist

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

    rtreelist = readrib(files)
    for rtree in rtreelist[1:]:
        for rnode in rtree:
            print("%s: %s" % (rnode.prefix, rnode.data["status"]))

