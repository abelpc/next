#!/bin/bash

DIR=samples/

if [ $# -eq 1 ]; then {
	EXPRESSION=".pcap.stats"
	file=$1

	hostname=`echo $file | awk -F $EXPRESSION '{print $1}'`
	#echo $hostname
	ip=`nslookup $hostname | grep -A 1 Address | grep -A 1 "\-\-" | grep Address | awk '{print $2}'`
        
	echo $ip
}
else {
	EXPRESSION=".pcap"

		for file in `ls`; do
		{
			hostname=`echo $file | awk -F $EXPRESSION '{print $1}'`
			ip=`nslookup $hostname | grep -A 1 Address | grep -A 1 "\-\-" | grep Address | awk '{print $2}'`

			echo $ip
		}
		done
}
fi

