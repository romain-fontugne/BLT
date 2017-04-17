#!/bin/bash

year=$1
for month in `seq -f %02g 1 12`
do
echo ${year}.${month}
rib=`/bin/ls -A /data/routeviews/archive.routeviews.org/route-views.isc/bgpdata/${year}.${month}/RIBS/ | grep rib.${year}${month}15| awk 'NR==1{print}'`
python ../blt.py /data/routeviews/archive.routeviews.org/route-views.isc/bgpdata/${year}.${month}/RIBS/${rib} /data/routeviews/archive.routeviews.org/route-views.isc/bgpdata/${year}.${month}/UPDATES/updates.${year}${month}15.* -o /home/tktbtk/Data/blt/${year}${month}15.blt
done

