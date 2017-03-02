import sys
from subprocess import Popen, PIPE
import glob
import radix
import hashlib
import argparse
import Queue

def PutBar(deno, mole, barlen):
    per = 100 * mole/deno
    perb = int(per/(100.0/barlen))

    s = "\r"
    s += "  |"
    s += "#" * perb
    s += "-" * (barlen - perb)
    s += "|"
    s += " " + (str(per) + "%").rjust(4)

    sys.stderr.write("%s ( %s / %s )" % (s, mole, deno))


def tagging(files, rtree, peers, timeflag, barflag, rib_time):

    if barflag == True:
        p1 = Popen(["bgpdump", "-m", "-v", files], stdout=PIPE, bufsize=-1)
        num_lines = sum(1 for line in p1.stdout)
    
    p1 = Popen(["bgpdump", "-m", "-v", files], stdout=PIPE, bufsize=-1)

    update_tag=""
    tagged_messages = ""
    num_update = 0
    num_withdraw = 0
    line_no = 1

    for line in p1.stdout:
        line = line.rstrip("\n")
        res = line.split('|',15)
        tags = ""
        if res[1] < rib_time:
            continue
        if peers.has_key(res[3]) is False:
            peers[res[3]] = dict()
       
        # Tag each message
        if res[2] == "W":
            zTd, zDt, zS, zOrig, zAS, zPfx  = res
            num_withdraw += 1
            node = rtree.search_exact(zPfx)
            if node is None or zOrig not in node.data:
                tags = tags + " #duplicate_withdraw"
                
            else:
                tags = tags + " #remove_prefix"
                node.data.pop(zOrig)
                if len(node.data) == 0:
                    rtree.delete(zPfx)
        else:
            zTd, zDt, zS, zOrig, zAS, zPfx, sPath, zPro, zOr, z0, z1, z2, z3, z4, z5 = res
            num_update += 1
            node = rtree.search_exact(zPfx)
            path_list = sPath.split(' ')
            origin_as = path_list[-1]
            message_h = hashlib.md5(z0 + z1 + z2 + z3 + z4 + z5).digest()           

            #new prefix
            if node is None or zOrig not in node.data:
                tags = tags + " #new_prefix"
                if node is None:
                    node = rtree.add(zPfx)
                node.data[zOrig] = dict()
                node.data[zOrig]["firsttime"] = zDt
                node.data[zOrig]["lasttime"] = zDt
                node.data[zOrig]["path"] = sPath
                node.data[zOrig]["community"] = z2
                node.data[zOrig]["MD5"] = message_h

            else:
                if sPath != node.data[zOrig]["path"]:
                    if origin_as != node.data[zOrig]["path"].split(" ")[-1]:
                        tags = tags + " #origin_change"
                    else:
                        tags = tags + " #path_change"

                    if node.data[zOrig]["MD5"] != message_h:
                        if node.data[zOrig]["community"] != z2:
                            tags = tags + " #community_change"
                        else:
                            tags = tags + " #attribute_change"
                else:
                    if node.data[zOrig]["MD5"] != message_h:
                        if node.data[zOrig]["community"] != z2:
                            tags = tags + " #community_change"
                        else:
                            tags = tags + " #attribute_change"
                    else: 
                        tags = tags + " #duplicate_announce"

                        # Table Transfer Tag
                        Dt = int(zDt)
                        for Ts in list(peers[zOrig]["queues"]): 
                            if Dt - Ts >= 60:
                                peers[zOrig]["queues"].pop()
                            else:
                                break
                        peers[zOrig]["queues"].appendleft(Dt)
                        peers[zOrig]["sflags"]["before"] = peers[zOrig]["sflags"]["now"]
                        if len(peers[zOrig]["queues"]) >= 2000:
                            peers[zOrig]["sflags"]["now"] = 1
                        else:
                            peers[zOrig]["sflags"]["now"] = 0
                        if peers[zOrig]["sflags"]["before"] == 0 and peers[zOrig]["sflags"]["now"] == 1:
                            tags = tags + " #table_transfer"
                        
                # Update the radix
                node.data[zOrig]["lasttime"] = zDt
                node.data[zOrig]["path"] = sPath
                node.data[zOrig]["community"] = z2
                node.data[zOrig]["MD5"] = message_h 

            # Prepending Tag
            path_list_uniq = list(set(path_list))
            if len(path_list_uniq) != len(path_list):
                tags = tags + " #prepending"
            
        if timeflag == False:
            tagged_messages = tagged_messages + line + tags + "\n"
        else:
            tagged_messages = tagged_messages + res[1] +res[3] + res[5] + tags + "\n"
        
        if barflag == True:     
            PutBar(num_lines, line_no, 50)
            line_no += 1
    if barflag == True:
        sys.stderr.write("\n\n")
    return_list = [rtree, tagged_messages, peers, num_update, num_withdraw] 
    return return_list

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
