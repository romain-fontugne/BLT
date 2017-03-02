import sys
from subprocess import Popen, PIPE
import radix
import pickle
import argparse
import re
import readrib
import glob

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--traffic', help = 'analyze with traffic')
parser.add_argument("-b", "--blt_file", help = "import blt file")
parser.add_argument("-r", "--rib")
#parser.add_argument("-u", "updates", nargs = "*")

args = parser.parse_args()

pfx_data = {}
default_route = 0
regex = "\d+\.\d+\.\d+\.\d+"
pattern = re.compile(regex)
average_tree = radix.Radix()

#if args.blt_file != None:  
#	updates = open(args.blt_file, "r")
#else:
#	cmd = ["python", "blt.py", args.rib]
#	
#	for update in args.updates:
#	    cmd.append(update)
#	
#	updates = Popen(cmd, stdout=PIPE, bufsize=-1)

# READRIB

if args.traffic is not None:
    rib_files = glob.glob(args.rib)
    if len(rib_files)==0:
        print("RIB files not found! If you want to analyze traffic, you have to input rib!")
        sys.exit()
    rib_files.sort()
    for rf in rib_files:    
        print >> sys.stderr, "reading RIB now..."
        return_list = readrib.readrib(rf)
        rtreedict = return_list[0]

# UPDATES
updates = open(args.blt_file, "r")
for line in updates:
    line = line.split("\n")[0]
    if len(line) == 0 or "#" not in line:
        continue
    line, tag = line.split(" #")
    res = line.split('|')
    zPfx = res[5]
    zOrig = res[3]
    node = rtreedict[zOrig].search_exact(zPfx)
    if node is None or "tag" not in node.data:
        node = rtree.add(zPfx)
        node.data["tags"] = {}
        node.data["tags"]["message"]            =0
        node.data["tags"]["traffic_volume"]     =0
        node.data["tags"]["packets"]            =0
        node.data["tags"]["remove_prefix"]      =0
        node.data["tags"]["new_prefix"]         =0
        node.data["tags"]["community_change"]   =0
        node.data["tags"]["attribute_change"]   =0
        node.data["tags"]["other_change"]       =0
        node.data["tags"]["flapping"]           =0
        node.data["tags"]["prepending"]         =0
        node.data["tags"]["path_change"]        =0
        node.data["tags"]["origin_change"]      =0
        node.data["tags"]["duplicate_withdraw"] =0
        node.data["tags"]["duplicate_announce"] =0
        node.data["tags"]["table_transfer"]     =0
    node.data["tags"]["message"] += 1
    for tag in tags:
        node.data["tags"][tag] += 1
    
i = 0
for rtree in rtreedict:
    i+=1
    for node in rtree.nodes():
        if i == 1:
            anode = average_tree.search_exact(node.prefix)
            anode.data["message"]           = node.data["message"]
            anode.data["traffic_volume"]    = node.data["traffic_volume"]
            anode.data["packets"]           = node.data["packets"]
            anode.data["remove_prefix"]     = node.data["remove_prefix"]
            anode.data["new_prefix"]        = node.data["new_prefix"]
            anode.data["community_change"]  = node.data["community_change"]
            anode.data["attribute_change"]  = node.data["attribute_change"]
            anode.data["other_change"]      = node.data["other_change"]
            anode.data["flapping"]          = node.data["flapping"]
            anode.data["prepending"]        = node.data["prepending"]
            anode.data["path_change"]       = node.data["path_change"]
            anode.data["origin_change"]     = node.data["origin_change"]
            anode.data["duplicate_withdraw"]= node.data["duplicate_withdraw"]
            anode.data["duplicate_announce"]= node.data["duplicate_announce"]
            anode.data["table_transfer"]    = node.data["table_transfer"]
        else:
            anode = average_tree.search_exact(node.prefix)
            anode.data["message"]           =(anode.data["message"]           +node.data["message"])*(i-1)/i
            anode.data["traffic_volume"]    =(anode.data["traffic_volume"]    +node.data["traffic_volume"])*(i-1)/i
            anode.data["packets"]           =(anode.data["packets"]           +node.data["packets"])*(i-1)/i
            anode.data["remove_prefix"]     =(anode.data["remove_prefix"]     +node.data["remove_prefix"])*(i-1)/i
            anode.data["new_prefix"]        =(anode.data["new_prefix"]        +node.data["new_prefix"])*(i-1)/i
            anode.data["community_change"]  =(anode.data["community_change"]  +node.data["community_change"])*(i-1)/i
            anode.data["attribute_change"]  =(anode.data["attribute_change"]  +node.data["attribute_change"])*(i-1)/i
            anode.data["other_change"]      =(anode.data["other_change"]      +node.data["other_change"])*(i-1)/i
            anode.data["flapping"]          =(anode.data["flapping"]          +node.data["flapping"])*(i-1)/i
            anode.data["prepending"]        =(anode.data["prepending"]        +node.data["prepending"])*(i-1)/i
            anode.data["path_change"]       =(anode.data["path_change"]       +node.data["path_change"])*(i-1)/i
            anode.data["origin_change"]     =(anode.data["origin_change"]     +node.data["origin_change"])*(i-1)/i
            anode.data["duplicate_withdraw"]=(anode.data["duplicate_withdraw"]+node.data["duplicate_withdraw"])*(i-1)/i
            anode.data["duplicate_announce"]=(anode.data["duplicate_announce"]+node.data["duplicate_announce"])*(i-1)/i
            anode.data["table_transfer"]    =(anode.data["table_transfer"]    +node.data["table_transfer"])*(i-1)/i

# TRAFFIC
rib_traffic = 0
rib_route = 0
default_route = {"number" : 0, "traffic" : 0}
traffic = open(args.traffic, "r")
for line in traffic:
    if line.find("!") >= 0:
        continue
    line = line.translate(None,"\n").split(" ")
    label = line[0]
    value = int(line[1])
    if len(label) >= 16:
        print label
    if pattern.match(label) == None:
        print zPfx
        continue
    if label == "203.178.148.18" or label == "203.178.148.19":
        print "pfx = " + label
        continue
    else:
        node = rtree.search_best(label)
        if node == None:
            default_route["number"] += 1
            default_route["traffic"] += value
            continue
        else:
            rib_route += 1
            rib_traffic += value
            #print(label + "is in "+ node.prefix)
            node.data["tags"]["traffic_volume"] += value
            node.data["tags"]["packets"] +=1
print("default_route_number : " + str(default_route["number"]))
print("default_route_traffic : " + str(default_route["traffic"])) 
print("rib_route : " + str(rib_route))
print("rib_traffic : " + str(rib_traffic))
nodes = rtree.nodes()
for node in nodes:
    pfx_data[node.prefix] = node.data["tags"]

print pfx_data
