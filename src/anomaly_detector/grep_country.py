import argparse
import sys
import urllib2
import json

parser = argparse.ArgumentParser()
parser.add_argument("blt")
parser.add_argument("CN")
args = parser.parse_args()

url = "http://geoinfo.bgpmon.io/201701/prefixes_announced_from_country/" + args.CN
response = urllib2.urlopen(url)
data = json.load(urllib2.urlopen(url))
prefixes = list()
for d in data:
  prefixes.append(d["BGPPrefix"])

with open(args.blt, "r") as f:
  for line in f:
    res = line.split("|")
    if len(res) == 6:
      res[5] = res[5].split(" #")[0] 
    if res[5] in prefixes:
      sys.stdout.write(line)
    else:
      continue
