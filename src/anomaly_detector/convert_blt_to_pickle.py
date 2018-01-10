from datetime import datetime as dt
from datetime import timedelta as td
import glob
import argparse
import sys
import pickle
import csv


def convert(blt_file, outfile):

    tagCategory = ["duplicate_announce", "new_prefix", "transit_change", "community_change", "duplicate_withdrawal", "prepending_add", "prepending_change", "prepending_remove", "path_switching", "origin_change", "remove_prefix", "other_change"]

    pickleDictionary = dict()           # pickleDictionary[tagName][time] = [value]
    for tn in tagCategory:
        pickleDictionary[tn] = dict()

    for blt_file in blt_file:
        date = blt_file.split("/")[-1].split(".")[0]
        if "_" in date:
            date = date.split("_")[0]
        print "reading " + date + " now"

        blt_files = glob.glob(blt_file)
        
        if len(blt_files)==0:
            sys.exit()
                        
        blt_files.sort()

        initialAnalize = True
    #    BGP4MP|1421366399|A|195.66.225.76|251|207.150.172.0/22|251 1239 3257 21840|IGP|195.66.225.76|0|0|1239:321 1239:1000 1239:1004 65020:20202|NAG|| #new_prefix
        for bf in blt_files:
            blt = open(bf, "r")
            for line in blt:
                res = line.split(" #")
                message = res[0]
                _tagNames = res[1:]
                tagNames = list()
                for tagName in _tagNames:
                    tagNames.append(tagName.split("\n")[0])
                for tagName in tagNames:
                    if tagName not in tagCategory:
                        print "There is no [" + tagName + "] in this programs tagCategory."
                        continue

                timeStamp = dt.utcfromtimestamp(float(message.split("|")[1])).strftime("%Y/%m/%d %H:%M")
                timeStamp = dt.strptime(timeStamp, "%Y/%m/%d %H:%M")
                if initialAnalize == True:
                    preTime = timeStamp
                    initialAnalize = False

                while timeStamp > preTime + td(minutes=1):
                    for tc in tagCategory:
                        pickleDictionary[tc][preTime + td(minutes=1)] = 0
                    preTime += td(minutes=1)

                for tagName in tagNames:
                    if timeStamp not in pickleDictionary[tagName]:
                        for tc in tagCategory:
                            pickleDictionary[tc][timeStamp] = 0

                    pickleDictionary[tagName][timeStamp] += 1
                preTime = timeStamp
        
        
    with open(outfile, "wb") as f:
        pickle.dump(pickleDictionary, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("blt_file", help = "import blt file", nargs = "*")
    args = parser.parse_args()
    pickle_file = args.blt_file[0].split(".")[0] + ".pkl"
    convert(args.blt_file, pickle_file)
