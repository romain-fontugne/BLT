import sys
from subprocess import Popen, PIPE
import glob
import radix
import readrib
import tagging
import argparse

if __name__ == "__main__":
	
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tag', help = 'desplay only timestamps and tags', action = 'store_true')
    parser.add_argument('-o', '--outfile', help = 'output text file')
    parser.add_argument("rib")
    parser.add_argument("updates", nargs = "*")

    args = parser.parse_args()
    
    if args.outfile != None:
        f = open(args.outfile, "w")
    
    update_no = 0
    withdraw_no = 0 

    if len(args.rib)+len(args.updates) < 2:
        print >> sys.stderr, ("usage: %s ribfiles*.bz2 updatefiles*.bz2" % sys.argv[0])
        sys.exit()
	
    # read rib files
    rib_files = glob.glob(args.rib)
	
    if len(rib_files)==0:
        print("Files not found!")
        sys.exit()

    rib_files.sort()
    print >> sys.stderr, "reading RIB now..."
    rtreedict = readrib.readrib(rib_files)
    # read update files and tag them
    for update in args.updates:
        print >> sys.stderr, "reading %s now..." % update

        update_files = glob.glob(update)
	
        if len(update_files)==0:
            sys.exit()
			
        update_files.sort()

        return_list = tagging.tagging(update_files, args.tag, rtreedict)
        rtreedict = return_list[0]
        update_no += return_list[2]
        withdraw_no += return_list[3]
        
        if args.outfile != None:
            f.write(return_list[1])
        else:
            print return_list[1]
        
    if args.outfile != None:
        f.close()

    print >> sys.stderr, "\n\n" + "#peers = " +  str(len(rtreedict))
    print >> sys.stderr, "#updates = " + str(update_no)
    print >> sys.stderr, "#withdraws = " + str(withdraw_no)
