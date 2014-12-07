#!/bin/bash

DIR=samples/

if [ $# -eq 1 ]; then {
	EXPRESSION=".1.monitor.pcap"
	file=$1

	hostname=`echo $file | awk -F $EXPRESSION '{print $1}'`
	#echo $hostname
	ip=`nslookup $hostname | grep -A 1 Address | grep -A 1 "\-\-" | grep Address | awk '{print $2}'`
        
	echo $ip
}
else {
	pushd $DIR >> /dev/null
	EXPRESSION=".1.monitor.pcap"
	DIR_FILES=(`ls -d */`)

	for dir in $DIR_FILES; do
	{
		pushd $dir >> /dev/null
		FILES=(`ls`)

		for file in ${FILES[@]}; do
		{
			hostname=`echo $file | awk -F $EXPRESSION '{print $1}'`
			ip=`nslookup $hostname | grep -A 1 Address | grep -A 1 "\-\-" | grep Address | awk '{print $2}'`

			echo $ip
		}
		done

		popd >> /dev/null
	}
	done

	popd >> /dev/null
}
fi

