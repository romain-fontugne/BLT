import datetime as dt
import glob
import argparse
import sys
import pickle
import csv


parser = argparse.ArgumentParser()
parser.add_argument("-b", "--blt_file", help = "import blt file", nargs = "*")
parser.add_argument("-o", "--outfile", help="output file")
parser.add_argument("-r", "--ratio_mode", action="store_true")

args = parser.parse_args()

pfx_data = {}
tags_all = dict()
tags_all_peers = dict()
default_route = 0

if args.blt_file is None:
    sys.stderr.write("There is no blt_file. Please input it")
    sys.exit()


#print "date messages duplicate_announce new_prefix attribute_change path_change community_change duplicate_withdraw prepending origin_change remove_prefix"
tag_name = ["duplicate_announce", "new_prefix", "attribute_change", "path_change", "community_change", "duplicate_withdraw", "prepending_add", "prepending_change", "prepending_remove", "path_switching", "origin_change", "remove_prefix", "other_change"]
for blt_file in args.blt_file:
    date = blt_file.split("/")[-1].split(".")[0]
    if "_" in date:
        date = date.split("_")[0]
    print "reading " + date + " now"
#20140715.blt
    blt_files = glob.glob(blt_file)
    
    if len(blt_files)==0:
        sys.exit()
                    
    blt_files.sort()
    messages = 0
    dates = list()
    tags = dict()
    tag_peers = dict()
    tag_peers["messages"] = dict()
#    BGP4MP|1421366399|A|195.66.225.76|251|207.150.172.0/22|251 1239 3257 21840|IGP|195.66.225.76|0|0|1239:321 1239:1000 1239:1004 65020:20202|NAG|| #new_prefix
    for bf in blt_files:
        blt = open(bf, "r")
        for line in blt:

            try:
                date = dt.datetime.fromtimestamp(float(line.split("|")[1]))-dt.timedelta(hours = 9)
            except:
                print line
                sys.exit()
            if date.strftime("%Y%m%d_%H%M") not in dates:
                print date
                dates.append(date.strftime("%Y%m%d_%H%M"))
                if len(tags.items()) != 0:
                    for tag in tags.items():
                        if args.ratio_mode == True:
                            tags[tag[0]] = float(tag[1])/ messages
                        else:
                            tags[tag[0]] = tag[1]

                        #print tag[0] + " : " + str(tags[tag[0]])
                    for tag in tag_peers.items():
                        if tag[0] == "messages":
                            continue
                        for peer in tag[1].keys():
                            if args.ratio_mode == True:
                                tag_peers[tag[0]][peer] = float(tag[1][peer]) / tag_peers["messages"][peer] 
                            else:
                                tag_peers[tag[0]][peer] = tag[1][peer]
                    tags_all[date] = tags
                    tags_all_peers[date] = tag_peers
                tags = dict()
                for t in tag_name:
                    tags[t] = 0
                tag_peers = dict()
                tag_peers["messages"] = dict()
                messages = 0
            messages += 1
            tag = line.split("\n")[0].split(" #")
            peer = tag[0].split("|")[3]
            tag.pop(0)
            for t in tag:
                if t not in tag_peers:
                    tag_peers[t] = dict()
                if peer not in tag_peers[t]:
                    tag_peers[t][peer] = 0 
                tag_peers[t][peer] += 1

                if peer not in tag_peers["messages"]:
                    tag_peers["messages"][peer] = 0
                tag_peers["messages"][peer] += 1 

            for t in tag:
                if t not in tags:
                    tags[t] = 0
                tags[t] += 1
        
        #print blt_file.split("/")[-1].split(".")[0] + " " + str(messages) + " " + ' '.join(map(str,tags.values()))
        #print (" ")
        #for tag in tag_peers.items():
        #    print tag[0] + " : "
        #    print tag[1]
        #    print (" ")
        
        
pkl_file = args.outfile + ".pkl"
with open(pkl_file, mode = "wb") as f:
    pickle.dump(tags_all, f)
pkl_peer = args.outfile + "_peers.pkl"
with open(pkl_peer, mode = "wb") as g:
    pickle.dump(tags_all_peers, g)

