import sys

tagging = ["remove_prefix", "new_perifx", "community_change", "other_change", "flapping", "prepending", "origin_change", "path_change", "duplicate_withdraw", "duplicate_announce", "session_reset", "attribute_change"]
ktag = dict()
for t in tagging:
    ktag[t] = list()

f = open(sys.argv[1], "r")
for line in f:
    tags = line.split("\n")[0].split("#")
    tags.pop(0)
    # new_prefix
    
    for t in tagging:
        for tag in tags:
            if t in tags:
                tags.remove(t)
                if tag not in ktag[t]:
                    ktag[t].append(tag)

print ktag






#new_prefix haihan

