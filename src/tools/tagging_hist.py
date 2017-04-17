import sys
from subprocess import Popen, PIPE
import glob
import radix
import hashlib
import argparse
import Queue
import pickle
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


def tagging(files, rtree, with_tree, peers, timeflag, barflag, rib_time, outfile, path_len, path_len_dup):
    if barflag == True:
        p1 = Popen(["bgpdump", "-m", "-v", files], stdout=PIPE, bufsize=-1)
        num_lines = sum(1 for line in p1.stdout)
    
    p1 = Popen(["bgpdump", "-m", "-v", files], stdout=PIPE, bufsize=-1)

    update_tag=""
    tagged_messages = ""
    num_update = 0
    num_withdraw = 0
    line_no = 1
    i = 0


    if outfile != "":
        f = open(outfile, "a")
    dup = 0
    remove = 0
    for line in p1.stdout:
       # time1 = dt.now()
        
        line = line.rstrip("\n")
        res = line.split('|',15)
        tags = ""
        if res[1] < rib_time:
            continue
        if peers.has_key(res[3]) is False:
            peers[res[3]] = dict()
      #  time2 = dt.now()
      #  delta1 = (time2-time1).total_seconds()
      #  sys.stderr.write("debug :all :  "  + str(i) + " " + str(delta1) + "\n")
       
        # Tag each message
        if res[2] == "W":
        #    time1 = dt.now()
            
            zTd, zDt, zS, zOrig, zAS, zPfx  = res
            num_withdraw += 1
            node = rtree.search_exact(zPfx)
            wnode = with_tree.search_exact(zPfx)
            if node is None or zOrig not in node.data:
                tags = tags + " #duplicate_withdraw"
                dup += 1
                # BGP4MP|1300152223|W|195.66.224.99|13237|175.136.156.0/22
                if wnode == None:
                    continue
                else:
                    if wnode.data["path_length"] not in path_len_dup.keys():
                        path_len_dup[wnode.data["path_length"]] = 0
                    path_len_dup[wnode.data["path_length"]] += 1
            else:
                remove += 1
                tags = tags + " #remove_prefix"
                if wnode == None:
                    wnode = with_tree.add(zPfx)
                path_length = len(node.data[zOrig]["path"].split())
                wnode.data["path_length"] = path_length
                node.data.pop(zOrig)
                if len(node.data) == 0:
                    rtree.delete(zPfx)
                

                if path_length not in path_len.keys():
                    path_len[path_length] = 0
                path_len[path_length] += 1
                
                    
        #    time2 = dt.now()
        #    delta2 = (time2-time1).total_seconds()
        #    sys.stderr.write("debug :Withdraw :  "  + str(i) + " " + str(delta2) + "\n")
        
        else:
        #    time1 = dt.now()
            zTd, zDt, zS, zOrig, zAS, zPfx, sPath, zPro, zOr, z0, z1, z2, z3, z4, z5 = res
            node = rtree.search_exact(zPfx)
            #new prefix
            if node is None or zOrig not in node.data:
                time3 = dt.now()
                tags = tags + " #new_prefix"
                if node is None:
                    node = rtree.add(zPfx)
                node.data[zOrig] = dict()
                node.data[zOrig]["path"] = sPath
                wnode = with_tree.search_exact(zPfx)
                if wnode != None:
                    with_tree.delete(zPfx)
            else:
                continue


        
        if barflag == True:     
            PutBar(num_lines, line_no, 50)
            line_no += 1
        #time10 = dt.now()
        #delta9 = (time10-time9).total_seconds()
        #sys.stderr.write("debug :footer :  "  + str(i) + " " + str(delta9) + "\n")
        #time2 = dt.now()
        #delta10 = (time2-time1).total_seconds()
        #sys.stderr.write("debug :Update :  "  + str(i) + " " + str(delta10) + "\n")
        i += 1
    if barflag == True:
        sys.stderr.write("\n\n")
    #return_list = [rtree, tagged_messages, peers, num_update, num_withdraw] 
    
    return_list = [rtree, peers, num_update, num_withdraw, path_len, path_len_dup, dup, remove, with_tree] 
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
