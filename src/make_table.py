import sys
from subprocess import Popen, PIPE
import radix
import pickle

rtree = radix.Radix()
pfx_data = {}

args = sys.argv
args.pop(0)
cmd = ["python", "blt.py"]

for arg in args:
    cmd.append(arg)

p1 = Popen(cmd, stdout=PIPE, bufsize=-1)
for line in p1.stdout:
    tags = []
    line = line.split("\n")[0]
    tags = line.split(" #")
    line = tags.pop(0)
    if len(line) == 0:
        continue
    
    res = line.split('|')
    zPfx = res[5]
    node = rtree.search_exact(zPfx)
    if node is None:
        node = rtree.add(zPfx)
        node.data["tags"] = {}
        node.data["tags"]["message"]=0
        node.data["tags"]["remove_prefix"]=0
        node.data["tags"]["new_prefix"]=0
        node.data["tags"]["community_change"]=0
        node.data["tags"]["attribute_change"]=0
        node.data["tags"]["other_change"]=0
        node.data["tags"]["flapping"]=0
        node.data["tags"]["prepending"]=0
        node.data["tags"]["path_change"]=0
        node.data["tags"]["origin_change"]=0
        node.data["tags"]["duplicate_withdraw"]=0
        node.data["tags"]["duplicate_announce"]=0
        node.data["tags"]["table_transfer"]=0
    node.data["tags"]["message"] += 1
    for tag in tags:
        node.data["tags"][tag] += 1
    
nodes = rtree.nodes()
for node in nodes:
    pfx_data[node.prefix] = node.data["tags"]



with open("test", mode="wb") as f:
    pickle.dump(pfx_data, f)
