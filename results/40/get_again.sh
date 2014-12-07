#!/bin/bash

KEY="/home/zekrioca/sopcast/planetlab-key"
NODES_DIR=nodes/
pushd $NODES_DIR


for x in `ls`; do
{
	while [ `du $x | awk '{print $1}'` -eq 0 ]; do
	{
		echo "$x is not okay"
		scp -i $KEY rnp_OSN@`echo $x | awk -F '.pcap.stats' '{print $1}'`:~/sopcast/results/$x .
	}
	done

	echo "$x is okay"
}
done
