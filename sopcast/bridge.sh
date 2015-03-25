#!/bin/bash

if [ ! $1 ]; then
{
	echo "$0 DIR CMD"
	exit -1
}
else {
	if [ ! $2 ]; then
	{
		echo "$0 DIR CMD"
		exit -1
	}
	else {
		if [ ! -d $1 ]; then
		{
			echo "DIR PROVIDED DOES NOT EXIST!"
			echo "$0 DIR CMD"
			exit -2
		}
		else {
			if [ ! -f $1/$2 ]; then
			{
				echo "CMD FILE PROVIDED DOES NOT EXIST!"
				echo "$0 DIR CMD"
				exit -3
			}
			fi
		}
		fi
	}
	fi
}
fi

TSHARK=/usr/sbin/tshark
INTERFACE=eth0
#DIR=/home/rnp_OSN/sopcast
DIR=$1
CMD=$2
RESULTS=$DIR/samples
FILE_NAME=`hostname`.pcap

pushd $DIR 1>/dev/null 2>&1

if [ ! -d $RESULTS ]; then
{
	mkdir $RESULTS
}
else {
	sudo rm -r $RESULTS
	mkdir $RESULTS
}
fi

touch $RESULTS/$FILE_NAME

sudo $TSHARK -q -i $INTERFACE -n -F libpcap -w $RESULTS/$FILE_NAME &

$DIR/$CMD
sudo chown -R $USER.slices $RESULTS 1>/dev/null 2>&1 
chown -R $USER.slices $RESULTS

sudo killall -9 -q $TSHARK 1>/dev/null 2>&1

sleep 10
sh create_analisys.sh

popd 1>/dev/null 2>&1
