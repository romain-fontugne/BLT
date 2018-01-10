import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("blt")
parser.add_argument("asn")
args = parser.parse_args()


with open(args.blt, "r") as f:
  for line in f:
    res = line.split("|")
    if len(res) == 6: #"withdraw"
      if res[4] == args.asn:
        sys.stdout.write(line)
      continue
    as_path = res[6]
    if args.asn in as_path.split(" "):
      sys.stdout.write(line)
