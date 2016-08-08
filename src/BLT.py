import sys
from subprocess import Popen, PIPE
import glob
import radix
import readrib
import tagging
import copy


if __name__ == "__main__":
	
	arguments=sys.argv
	if len(arguments) < 3:
		print("usage: %s ribfiles*.bz2 updatefiles*.bz2" % arguments[0])
		sys.exit()
	
	arguments.pop(0)
		
	# list rib files
	rib_files = glob.glob(arguments[0])
	
	if len(rib_files)==0:
		print("Files not found!")
		sys.exit()

	rib_files.sort()

	rtree=readrib.readrib(rib_files)

	arguments.pop(0)
	
	for arg in arguments:
		
		update_files = glob.glob(arg)
	
		if len(update_files)==0:
			sys.exit()
			
		update_files.sort()

		rtree=tagging.tagging(update_files,rtree)

#	for node in rtree:
#		print("%s: %s" % (node.prefix, node.data["path"]))
