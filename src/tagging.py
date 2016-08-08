import sys
from subprocess import Popen, PIPE
import glob
import radix

def tagging(files, rtree=radix.Radix()):

    p0 = Popen(["bzcat"]+files, stdout=PIPE, bufsize=-1)
    p1 = Popen(["bgpdump", "-m", "-v", "-"], stdin=p0.stdout, stdout=PIPE, bufsize=-1)
    
    for line in p1.stdout:
        line=line.rstrip("\n")
        res = line.split('|',15)
        if res[2] == "W":
            node = rtree.search_exact(res[5])
            
            if node is None:
                line = "    # ".join([line,"Duplicate Withdraw"])
            
            else:
                line = "    # ".join([line,"Delete"])
                node=rtree.delete(res[5])
        
        else:
            zTd, zDt, zS, zOrig, zAS, zPfx, sPath, zPro, zOr, z0, z1, z2, z3, z4, z5 = res
            node = rtree.search_exact(zPfx)
            
            # Prepending Tag
            path_list = sPath.split(' ')
            path_list_uniq = list(set(path_list))
            if len(path_list_uniq) != len(path_list):
                line = "   # ".join([line,"Prepending"])

            if node is None:
                line = "    # ".join([line,"New Prefix"])
                node = rtree.add(zPfx)
                node.data["firsttime"] = zDt
                node.data["lasttime"] = zDt
                node.data["path"] = sPath
            
            else:
                if sPath != node.data["path"]:
                    if path_list[-1] != node.data["path"].split(" ")[-1]:
                        line = "   # ".join([line,"Origin Change"])
                    else:
                        line = "   # ".join([line,"Path Change"])
                    node.data["lasttime"] = zDt
                    node.data["path"] = sPath
                
                else:
                    line = "   # ".join([line,"Duplicate Announce"])
                    node.data["lasttime"] = zDt 
        print line
    return rtree

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("usage: %s updatefiles*.bz2" % sys.argv[0])
        sys.exit()
        
    # list update files
    files = glob.glob(sys.argv[1])
    if len(files)==0:
        print("Files not found!")
        sys.exit()

    files.sort()

    rtree = tagging(files)

    # Print the radix tree
    for rnode in rtree:
        print("%s: %s" % (rnode.prefix, rnode.data["path"]))
