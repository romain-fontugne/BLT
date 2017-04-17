import sys
from subprocess import Popen, PIPE
import glob
import radix
import readrib
import tagging_hist
import argparse
import time
import datetime
import pickle

if __name__ == "__main__":
	
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tag', help = 'desplay only timestamps and tags', action = 'store_true')
    parser.add_argument('-o', '--outfile', help = 'output text file')
    parser.add_argument('-b', '--bar', help = 'show the progress bar', action = 'store_true')
    parser.add_argument("rib")
    parser.add_argument("updates", nargs = "*")

    args = parser.parse_args()
    
    if args.outfile == None:
        outfile = ""
    else:
        outfile = args.outfile
    
    num_update = 0
    num_withdraw = 0 

    if len(args.rib)+len(args.updates) < 2:
        print >> sys.stderr, ("usage: %s ribfiles*.bz2 updatefiles*.bz2" % sys.argv[0])
        sys.exit()
	
    # read rib files
    rib_file = args.rib
	
    if len(rib_file)==0:
        print("Files not found!")
        sys.exit()
    rib_time_ = rib_file.split("/")[-1][4:16]
    rib_time = datetime.datetime.strptime(rib_time_, "%Y%m%d.%H%M")
    file_time = str(rib_time.strftime("%Y%m%d"))
    rib_time = int(time.mktime(rib_time.timetuple()))

    print >> sys.stderr, "reading RIB now..."

    return_list = readrib.readrib(rib_file)

    rtree = return_list[0]
    peers = return_list[1]
    dup = 0
    remove = 0
    # read update files and tag them
    path_len = dict()
    path_len_dup = dict()
    with_tree = radix.Radix()
    for update in args.updates:
        print >> sys.stderr, "reading %s now..." % update

        update_files = glob.glob(update)
	
        if len(update_files)==0:
            sys.exit()
			
        update_files.sort()
        for uf in update_files:
            return_list = tagging_hist.tagging(uf, rtree, with_tree, peers, args.tag, args.bar,rib_time, outfile, path_len, path_len_dup)

            rtree = return_list[0]
            # tagged_messages = return_list[1]
            peers = return_list[1]
            num_update += return_list[2]
            num_withdraw += return_list[3]
            path_len = return_list[4]
            path_len_dup = return_list[5]
            dup += return_list[6]
            remove += return_list[7]
            with_tree = return_list[8]
            
    print "remove = " + str(remove)
    print "duplicate = " + str(dup)
    print "path_len:"
    print path_len
    print "\npath_len_dup:"
    print path_len_dup
    path_len_list = [path_len, path_len_dup]
    with open("/home/tktbtk/Data/aspath_hist_data_" + file_time +".pkl", "wb") as f:
        pickle.dump(path_len_list, f)
    

    

            #if args.outfile != None:
            #    f.write(tagged_messages)
            #else:
            #    print tagged_messages
        
    #if args.outfile != None:
    #    f.close()

    print >> sys.stderr, "\n\n" + "#peers = " +  str(len(peers))
    print >> sys.stderr, "#updates = " + str(num_update)
    print >> sys.stderr, "#withdraws = " + str(num_withdraw)
