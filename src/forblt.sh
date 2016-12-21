#!/bin/bash

year=2016
month=12
for year in `seq 2010 2015`
do
    for month in `seq 1 12`
    do
        rib=`/bin/ls -A /data/routeviews/archive.routeviews.org/route-views.linx/bgpdata/${year}.${month}/RIBS/ | grep rib.${year}${month}15| awk 'NR==1{print}'`
        python blt.py /data/routeviews/archive.routeviews.org/route-views.linx/bgpdata/${year}.${month}/RIBS/${rib} /data/routeviews/archive.routeviews.org/route-views.linx/bgpdata/${year}.${month}/UPDATES/update.${year}${month}15* -o /home/tktbtk/Data/blt/blt_${year}${month}15 &
    done
    wait
done

