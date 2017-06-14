#!/bin/bash

year=$1
for month in `seq -f %02g 1 12`
do
echo ${year}.${month}
rib=`/bin/ls -A /data/routeviews/archive.routeviews.org/route-views.linx/bgpdata/${year}.${month}/RIBS/ | grep rib.${year}${month}15| awk 'NR==1{print}'`
python2 peers.py /data/routeviews/archive.routeviews.org/route-views.linx/bgpdata/${year}.${month}/RIBS/${rib}
done

