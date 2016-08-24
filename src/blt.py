import sys
from subprocess import Popen, PIPE
import glob
import radix
import readrib
import tagging
import argparse

if __name__ == "__main__":
	
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--tag', help = 'desplay only timestamps and tags'
                        , action = 'store_true')
    parser.add_argument("rib")
    parser.add_argument("updates", nargs = "*")

    args = parser.parse_args()

    if len(args.rib)+len(args.updates) < 2:
        print("usage: %s ribfiles*.bz2 updatefiles*.bz2" % sys.argv[0])
        sys.exit()
	
    # read rib files
    rib_files = glob.glob(args.rib)
	
    if len(rib_files)==0:
        print("Files not found!")
        sys.exit()

    rib_files.sort()
    rtreedict = readrib.readrib(rib_files)

    # read update files and tag them
    for update in args.updates:
		
        update_files = glob.glob(update)
	
        if len(update_files)==0:
            sys.exit()
			
        update_files.sort()

        rtreedict = tagging.tagging(update_files, args.tag, rtreedict)

        # print update_tag
