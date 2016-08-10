import sys
from subprocess import Popen, PIPE
import glob
import radix
import hashlib

def tagging(files, rtree=radix.Radix()):

    p0 = Popen(["bzcat"]+files, stdout=PIPE, bufsize=-1)
    p1 = Popen(["bgpdump", "-m", "-v", "-"], stdin=p0.stdout, stdout=PIPE, bufsize=-1)
    update_tag=""

    for line in p1.stdout:
        line=line.rstrip("\n")
        res = line.split('|',15)
        
        if res[2] == "W":
            node = rtree.search_exact(res[5])
            
            # Duplicate Withdraw Tag
            if node is None:
                line = line + " #duplicate_withdraw"
            
            # Delete Tag
            else:
                line = line + " #delete"
                node=rtree.delete(res[5])
        
        else:
            zTd, zDt, zS, zOrig, zAS, zPfx, sPath, zPro, zOr, z0, z1, z2, z3, z4, z5 = res
            node = rtree.search_exact(zPfx)
            
            # Prepending Tag
            path_list = sPath.split(' ')
            path_list_uniq = list(set(path_list))
            if len(path_list_uniq) != len(path_list):
                line = line + " #prepending"
            
            # New Prefix Tag
            if node is None:
                line = line + " #new_prefix"
                node = rtree.add(zPfx)
                node.data["firsttime"] = zDt
                node.data["lasttime"] = zDt
                node.data["path"] = sPath
                node.data["community"] = z2
                node.data["MD5"] = hashlib.md5(zTd + zS + zOrig + zPfx + sPath + zPro + zOr + z0 + z1 + z2 + z3 + z4 + z5).digest()

            else:
                # Path Change, Origin Change
                if sPath != node.data["path"]:
                    if path_list[-1] != node.data["path"].split(" ")[-1]:
                        line = line + " #origin_change"
                    else:
                        line = line + " #path_change"
                    node.data["lasttime"] = zDt
                    node.data["path"] = sPath
                    node.data["MD5"] = hashlib.md5(zTd + zS + zOrig + zPfx + sPath + zPro + zOr + z0 + z1 + z2 + z3 + z4 + z5).digest()
                
                # Duplicate Announce, Community Change, Attribute Change 
                
                else:
                    message_h = hashlib.md5(zTd + zS + zOrig + zPfx + sPath + zPro + zOr + z0 + z1 + z2 + z3 + z4 + z5).digest()
                    if node.data["MD5"] == message_h:
                        line = line + " #duplicate_announce"
                        node.data["lasttime"] = zDt

                    elif node.data["community"] != z2:
                        line = line + " #community_change"
                        node.data["community"] = z2
                        node.data["lasttime"] = zDt
                    else:
                        line = line + " #attribute_change"
                        node.data["lasttime"] = zDt
                        node.data["MD5"] = message_h
        
        update_tag = "\n".join([update_tag,line])
    
    return [rtree, update_tag]

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

    rtree, update_tag = tagging(files)

    # Print the update_tag
    print update_tag
