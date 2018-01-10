import sys
from subprocess import Popen, PIPE
import glob
import radix
import readrib
import tagging
import argparse
import time
import datetime
import calendar

if __name__ == "__main__":
	
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tag', help = 'desplay only timestamps and tags', action = 'store_true')
    parser.add_argument('-o', '--outfile', help = 'output text file')
    parser.add_argument('-v', '--version', help = 'if you want to analyze only ipv4 or ipv6')
    parser.add_argument('-s', '--startTime')
    parser.add_argument('-e', '--endTime')
    parser.add_argument('-c', '--collector')

    args = parser.parse_args()
    
    startTime = str(calendar.timegm(datetime.datetime.strptime(args.startTime, "%Y%m%d").utctimetuple()))
    endTime = str(calendar.timegm(datetime.datetime.strptime(args.endTime, "%Y%m%d").utctimetuple()))
    
    if args.outfile == None:
        outfile = ""
    else:
        outfile = args.outfile
    
    if args.version != None and args.version != "4" and args.version != "6":
        print "please input -v 6 or -v 4"
        sys.exit()


    num_update = 0
    num_withdraw = 0 

	
    # read rib files

    print >> sys.stderr, "reading RIB now..."

    return_list = readrib.readrib(startTime, args.collector, args.version)

    rtree = return_list[0]
    peers = return_list[1]
    rib_time = return_list[2]

    # read update files and tag them

    print >> sys.stderr, "reading UPDATE now..."
    return_list = tagging.tagging(rtree, peers, args.tag, rib_time, outfile, args.version, startTime, endTime, args.collector)
    rtree = return_list[0]
    peers = return_list[1]
    num_update += return_list[2]
    num_withdraw += return_list[3]


    print >> sys.stderr, "\n\n" + "#peers = " +  str(len(peers))
    print >> sys.stderr, "#updates = " + str(num_update)
    print >> sys.stderr, "#withdraws = " + str(num_withdraw)
