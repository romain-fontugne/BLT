import sys
import time

def PutBar(per, barlen):
    perb = int(per/(100.0/barlen))

    s = "\r"
    s += "|"
    s += "#" * perb
    s += "-" * (barlen - perb)
    s += "|"
    s += " " + (str(per) + "%").rjust(4)

    sys.stderr.write(s)

if __name__ == "__main__":
    for per in range(200):
        PutBar(per/2, 50)
        time.sleep(0.1)

    PutBar(100,50)
