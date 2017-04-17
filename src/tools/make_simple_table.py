import glob
import argparse
import sys
import pickle
import csv


parser = argparse.ArgumentParser()
parser.add_argument("-b", "--blt_file", help = "import blt file", nargs = "*")

args = parser.parse_args()

pfx_data = {}
tags_all = dict()
tags_all_peers = dict()
default_route = 0

if args.blt_file is None:
    sys.stderr.write("There is no blt_file. Please input it")
    sys.exit()


#print "date messages duplicate_announce new_prefix attribute_change path_change community_change duplicate_withdraw prepending origin_change remove_prefix"
for blt_file in args.blt_file:
    date = blt_file.split("/")[-1].split(".")[0]
    print "reading " + date + " now"
    tags = dict()
#20140715.blt
    blt_files = glob.glob(blt_file)
    
    if len(blt_files)==0:
        sys.exit()
                    
    blt_files.sort()
    messages = 0
    tag_peers = dict()
    tag_peers["messages"] = dict()
#    BGP4MP|1421366399|A|195.66.225.76|251|207.150.172.0/22|251 1239 3257 21840|IGP|195.66.225.76|0|0|1239:321 1239:1000 1239:1004 65020:20202|NAG|| #new_prefix
    for bf in blt_files:
        blt = open(bf, "r")
        for line in blt:
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

        for tag in tags.items():
            tags[tag[0]] = float(tag[1])/ messages
        for tag in tag_peers.items():
            if tag[0] == "messages":
                continue
            for peer in tag[1].keys():
                tag_peers[tag[0]][peer] = float(tag[1][peer]) / tag_peers["messages"][peer] 
            #print tag[0]
            #print tag_peers[tag[0]][peer]
            #print " "
        tags_all[date] = tags
        tags_all_peers[date] = tag_peers
        #print blt_file.split("/")[-1].split(".")[0] + " " + str(messages) + " " + ' '.join(map(str,tags.values()))
        #print (" ")
        #for tag in tag_peers.items():
        #    print tag[0] + " : "
        #    print tag[1]
        #    print (" ")
        
        
pkl_file = "/home/tktbtk/Data/pickel/2005-2016_normal.pkl"
with open(pkl_file, mode = "wb") as f:
    pickle.dump(tags_all, f)
pkl_peer = "/home/tktbtk/Data/pickel/2005_2016_normal_peers.pkl"
with open(pkl_peer, mode = "wb") as g:
    pickle.dump(tags_all_peers, g)

