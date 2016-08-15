import sys
from subprocess import Popen, PIPE
import glob
import radix
import hashlib

def tagging(files, rtreedict = {}):

    p0 = Popen(["bzcat"]+files, stdout=PIPE, bufsize=-1)
    p1 = Popen(["bgpdump", "-m", "-v", "-"], stdin=p0.stdout, stdout=PIPE, bufsize=-1)
    update_tag=""
    
    
    for line in p1.stdout:
        line=line.rstrip("\n")
        res = line.split('|',15)
        zOrig = res[3]
        
        if rtreedict.has_key(zOrig) is False:
            rtreedict[zOrig] = radix.Radix()
       
        # Tag each message
        if res[2] == "W":
            if rtreedict[zOrig].search_exact(res[5]) is None:
                line = line + " #duplicate_withdraw"
            
            else:
                line = line + " #remove_prefix"
                rtreedict[zOrig].delete(res[5])
        
        else:
            zTd, zDt, zS, zOrig, zAS, zPfx, sPath, zPro, zOr, z0, z1, z2, z3, z4, z5 = res
            node = rtreedict[zOrig].search_exact(zPfx)
            path_list = sPath.split(' ')
            origin_as = path_list[-1]
            

            if node is None:
                line = line + " #new_prefix"
                node = rtreedict[zOrig].add(zPfx)
                node.data["firsttime"] = zDt
                node.data["lasttime"] = zDt
                node.data["path"] = sPath
                node.data["community"] = z2
                node.data["MD5"] = hashlib.md5(z0 + z1 + z2 + z3 + z4 + z5).digest()

            else:
                message_h = hashlib.md5(z0 + z1 + z2 + z3 + z4 + z5).digest()

                if sPath != node.data["path"]:
                    if origin_as != node.data["path"].split(" ")[-1]:
                        line = line + " #origin_change"
                    else:
                        line = line + " #path_change"
                        node.data["lasttime"] = zDt
                        node.data["path"] = sPath
                        node.data["MD5"] = hashlib.md5(z0 + z1 + z2 + z3 + z4 + z5).digest()

                    if node.data["MD5"] != message_h:
                        if node.data["community"] != z2:
                            line = line + " #community_change"
                            node.data["community"] = z2
                            node.data["lasttime"] = zDt
                        else:
                            line = line + " #attribute_change"
                            node.data["lasttime"] = zDt
                            node.data["MD5"] = message_h
                else:
                    if node.data["MD5"] != message_h:
                        if node.data["community"] != z2:
                            line = line + " #community_change"
                            node.data["community"] = z2
                            node.data["lasttime"] = zDt
                        else:
                            line = line + " #attribute_change"
                            node.data["lasttime"] = zDt
                            node.data["MD5"] = message_h
                    else:
                        line = line + " #duplicate_announce"
                        node.data["lasttime"] = zDt
            # Prepending Tag
            path_list_uniq = list(set(path_list))
            if len(path_list_uniq) != len(path_list):
                line = line + " #prepending"
        
        # update_tag = "\n".join([update_tag,line])
        print line

    return rtreedict

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

    rtreedict = tagging(files)

    # Print the update_tag
    # print update_tag
