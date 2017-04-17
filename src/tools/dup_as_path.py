import argparse
import sys
import glob
import pickle


parser = argparse.ArgumentParser()
parser.add_argument("-b", "--bltfiles", nargs = "*")
args = parser.parse_args()

bltfile = args.bltfiles
if len(bltfile) == 0:
    print "there is no blt. exit"
    sys.exit(0)

path_len = dict()
path_len["announce"] = dict()
path_len["duplicate"] = dict()


for blts in bltfile:
    blt_files = glob.glob(blts)

    blt_files.sort()

    for blt in blt_files:
        date = blt.split("/")[-1].split(".")[0]
        print >> sys.stderr, "reading %s now" % blt 
        f = open(blt, "r")
        for tline in f:
# BGP4MP|1421366400|A|2001:7f8:4::1b1b:1|6939|2a02:2158::/32|6939 13237 35226|IGP|2001:7f8:4::1b1b:1|0|0||NAG|| #new_prefix
            tline = tline.split("\n")[0]
            tline = tline.split(" #")
            line = tline[0]
            tline.pop(0)
            tag = tline

            res = line.split("|")
            if res[2] == "W":
                continue
            zTd, zDt, zS, zOrig, zAS, zPfx, sPath, zPro, zOr, z0, z1, z2, z3, z4, z5 = res

            pl = 0
            if tag == "duplicate_announce":
                if sPath not in path_len["duplicate"]:
                    path_len["duplicate"][sPath] = 0
                path_len["duplicate"][sPath] += 1
            else:
                if sPath not in path_len["announce"]:
                    path_len["announce"][sPath] = 0
                path_len["announce"][sPath] += 1


f = open("/home/tktbtk/Data/pickle/hist_announce_" + date +".png", "wb")
pickle.dump(path_len, f)
