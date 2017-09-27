import sys
import re
from subprocess import Popen, PIPE
import glob
import collections
import radix
import hashlib
import argparse
import Queue
from datetime import datetime as dt

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


def tagging(rtree, peers, timeflag,  rib_time, outfile, version, startTime, endTime, collector):

    dump = Popen(["bgpreader", "-w", startTime + "," + endTime, "-c", "route-views." + collector, "-m", "-t", "updates"], stdout=PIPE, bufsize=-1)

    update_tag=""
    tagged_messages = ""
    num_update = 0
    num_withdraw = 0
    line_no = 1
    i = 0
    
    v4 = r"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"

    if outfile != "":
        f = open(outfile, "a")

    for line in dump.stdout:
        
        line = line.rstrip("\n")
        res = line.split('|',15)
        tags = ""
        if res[1] < rib_time:
            continue
        if peers.has_key(res[3]) is False:
            peers[res[3]] = dict()

        if version == "4":
            if not re.match(v4, res[3]):
                continue
        elif version == "6":
            if re.match(v4, res[3]):
                continue
        if res[0] != "BGP4MP":
            continue
       
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
            try:
                zTd, zDt, zS, zOrig, zAS, zPfx, sPath, zPro, zOr, z0, z1, z2, z3, z4, z5 = res
            except:
                print "ignore " + line
                continue
            num_update += 1
            node = rtree.search_exact(zPfx)
            path_list = sPath.split(' ')
            origin_as = path_list[-1]
            message_h = hashlib.md5(z0 + z1 + z2 + z3 + z4 + z5).digest()           

            #new prefix
            if node is None or zOrig not in node.data:
                time3 = dt.now()
                tags = tags + " #new_prefix"
                if node is None:
                    node = rtree.add(zPfx)
                node.data[zOrig] = dict()
                node.data[zOrig]["firsttime"] = zDt
                node.data[zOrig]["lasttime"] = zDt
                node.data[zOrig]["path"] = sPath
                node.data[zOrig]["community"] = z2
                node.data[zOrig]["MD5"] = message_h
                node.data[zOrig]["old_path"] = ""

            else:
                time3 = dt.now()
                if sPath != node.data[zOrig]["path"]:
                    if origin_as != node.data[zOrig]["path"].split(" ")[-1]:
                        tags = tags + " #origin_change"
                    else:
                        tags = tags + " #path_change"
                        if node.data[zOrig]["old_path"] == sPath:
                            tags = tags + " #path_switching"
                        node.data[zOrig]["old_path"] = node.data[zOrig]["path"]

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
                        #for Ts in list(peers[zOrig]["queues"]): 
                        #    if Dt - Ts >= 60:
                        #        peers[zOrig]["queues"].pop()
                        #    else:
                        #        break
                        #peers[zOrig]["queues"].appendleft(Dt)
                        #peers[zOrig]["sflags"]["before"] = peers[zOrig]["sflags"]["now"]
                        #if len(peers[zOrig]["queues"]) >= 2000:
                        #    peers[zOrig]["sflags"]["now"] = 1
                        #else:
                        #    peers[zOrig]["sflags"]["now"] = 0
                        #if peers[zOrig]["sflags"]["before"] == 0 and peers[zOrig]["sflags"]["now"] == 1:
                        
                        #    tags = tags + " #table_transfer"
                        
                # Update the radix
                node.data[zOrig]["lasttime"] = zDt
                node.data[zOrig]["path"] = sPath
                node.data[zOrig]["community"] = z2
                node.data[zOrig]["MD5"] = message_h 

            # Prepending Tag
            path_list_uniq = list(set(path_list))
            if len(path_list_uniq) != len(path_list):
                old_path_list = collections.Counter(node.data[zOrig]["path"].split())
                new_path_list = collections.Counter(path_list)
                for new in new_path_list.items():
                    if new[1] > 1:
                        if new[0] not in old_path_list.keys():
                            tags = tags + " #prepending_add"
                        elif old_path_list[new[0]] == 1:
                            tags = tags + " #prepending_add"
                        elif old_path_list[new[0]] > 1 and new[1] != old_path_list[new[0]]:
                            tags = tags + " #prepending_change"
                    else:
                        if new[0] not in old_path_list:
                            continue
                        elif old_path_list[new[0]] > 1:
                            tags = tags + " #prepending_remove"
                
                
            
        if timeflag == False:
            if outfile == "":
                print line + tags 
            else:
                f.write(line + tags + "\n")
        else:
            if outfile == "":
                print res[1] + tags
            else:
                f.write(res[1] + tags + "\n")
        
        #time10 = dt.now()
        #delta9 = (time10-time9).total_seconds()
        #sys.stderr.write("debug :footer :  "  + str(i) + " " + str(delta9) + "\n")
        #time2 = dt.now()
        #delta10 = (time2-time1).total_seconds()
        #sys.stderr.write("debug :Update :  "  + str(i) + " " + str(delta10) + "\n")
        i += 1
    #return_list = [rtree, tagged_messages, peers, num_update, num_withdraw] 
    return_list = [rtree, peers, num_update, num_withdraw] 
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
