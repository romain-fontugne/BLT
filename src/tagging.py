import sys
from subprocess import Popen, PIPE
import glob
import radix
import hashlib
import argparse

def tagging(files, timeflag, rtreedict = {}):

    p0 = Popen(["bzcat"]+files, stdout=PIPE, bufsize=-1)
    p1 = Popen(["bgpdump", "-m", "-v", "-"], stdin=p0.stdout, stdout=PIPE, bufsize=-1)
    update_tag=""
    
    
    for line in p1.stdout:
        line = line.rstrip("\n")
        res = line.split('|',15)
        zOrig = res[3]
        tags = ""

        if rtreedict.has_key(zOrig) is False:
            rtreedict[zOrig] = radix.Radix()
       
        # Tag each message
        if res[2] == "W":
            if rtreedict[zOrig].search_exact(res[5]) is None:
                tags = tags + " #duplicate_withdraw"
            
            else:
                tags = tags + " #remove_prefix"
                rtreedict[zOrig].delete(res[5])
        
        else:
            zTd, zDt, zS, zOrig, zAS, zPfx, sPath, zPro, zOr, z0, z1, z2, z3, z4, z5 = res
            node = rtreedict[zOrig].search_exact(zPfx)
            path_list = sPath.split(' ')
            origin_as = path_list[-1]
            

            if node is None:
                tags = tags + " #new_prefix"
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
                        tags = tags + " #origin_change"
                    else:
                        tags = tags + " #path_change"
                        node.data["lasttime"] = zDt
                        node.data["path"] = sPath
                        node.data["MD5"] = hashlib.md5(z0 + z1 + z2 + z3 + z4 + z5).digest()

                    if node.data["MD5"] != message_h:
                        if node.data["community"] != z2:
                            tags = tags + " #community_change"
                            node.data["community"] = z2
                            node.data["lasttime"] = zDt
                        else:
                            tags = tags + " #attribute_change"
                            node.data["lasttime"] = zDt
                            node.data["MD5"] = message_h
                else:
                    if node.data["MD5"] != message_h:
                        if node.data["community"] != z2:
                            tags = tags + " #community_change"
                            node.data["community"] = z2
                            node.data["lasttime"] = zDt
                        else:
                            tags = tags + " #attribute_change"
                            node.data["lasttime"] = zDt
                            node.data["MD5"] = message_h
                    else:
                        tags = tags + " #duplicate_announce"
                        node.data["lasttime"] = zDt
                        line = line + " #path_change"

                # Update the radix
                node.data["lasttime"] = zDt
                node.data["path"] = sPath
                node.data["community"] = z2
                node.data["MD5"] = hashlib.md5(z0 + z1 + z2 + z3 + z4 + z5).digest()

            # Prepending Tag
            path_list_uniq = list(set(path_list))
            if len(path_list_uniq) != len(path_list):
                tags = tags + " #prepending"
        
        # print tagged messages
        if timeflag == False:
            print line + tags
        else:
            print res[1] + tags

    return rtreedict

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tag", help = "output only timestamps and tags"
                        , action = "store_true")
    parser.add_argument("updates", help = "desplay tagged messages of given update files"
                        , nargs = "*")
    args = parser.parse_args()
    
    if len(args.updates) < 1:
        print("usage: %s updatefiles*.bz2" % sys.argv[0])
        sys.exit()
    
    rtreedict = {}

   # list update files
    for update in args.updates:
        files = glob.glob(update)
        if len(files)==0:
            print("Files not found!")
            sys.exit()

        files.sort()

        rtreedict = tagging(files, args.tag, rtreedict)

    # Print the update_tag
    # print update_tag
