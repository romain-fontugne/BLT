import sys
from subprocess import Popen, PIPE
import glob
import radix

def readrib(files):
    
    rtree=radix.Radix()
    p0 = Popen(["bzcat"]+files, stdout=PIPE, bufsize=-1)
    p1 = Popen(["bgpdump", "-m", "-v", "-t", "change", "-"], stdin=p0.stdout, stdout=PIPE, bufsize=-1)

    for line in p1.stdout:
     	 
        res = line.split('|',15)
	zTd, zDt, zS, zOrig, zAS, zPfx, sPath, zPro, zOr, z0, z1, z2, z3, z4, z5 = res

        node = rtree.add(zPfx)
        node.data["firsttime"] = zDt
        node.data["lasttime"] = zDt
        node.data["path"] = sPath 

    return rtree

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

    rtree = readrib(files)

    # Print the radix tree
    for rnode in rtree:
        print("%s: %s" % (rnode.prefix, rnode.data["path"]))
