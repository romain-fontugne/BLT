from subprocess import PIPE, Popen
import re
import sys


p = Popen(["bgpdump", "-v", "-m", sys.argv[1]], stdout = PIPE)

v4 = r"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"
print re.match(v4, "192.168.1.5")

for line in p.stdout:
    #BGP4MP|1460757619|A|2001:7f8:4:1::e48f:1|58511|2001:898::/29|58511 15879|IGP|2001:7f8:4:1::e48f:1|0|0||NAG||
    res = line.split("|")
    if not re.match(v4, res[3]):
        if res[2] == "A":
            if re.match(v4, res[5].split("/")[0]): 
                print res


