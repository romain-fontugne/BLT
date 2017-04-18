from subprocess import Popen, PIPE
import sys


p1 = Popen(["bgpdump", "-m", "-v", sys.argv[1]], stdout=PIPE, bufsize=-1)

date = sys.argv[1].split("/")[-1].split(".")[1]
num_peers = 0
peers = list()
for line in p1.stdout:
   peer = line.split("|")[3] 
   if peer not in peers:
       num_peers += 1
       peers.append(peer)
f = open("/home/tktbtk/Data/peers.txt", "a")
f.write(date + " " + str(num_peers) +"\n")
