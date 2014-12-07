#!/bin/bash

URL="broker.sopcast.com"
PORT="3912"
CHANNEL="151684"
IN_PORT="3908"
OUT_PORT="8908"
HOME_DIR=~
SOP_DIR=$HOME_DIR/sopcast
RESULTS=$SOP_DIR/samples
TIMEOUT=$SOP_DIR/dependencies/timeout
SOP_EXE=$SOP_DIR/sp-auth/sp-sc-auth
TSHARK=/usr/sbin/tshark
NUM_SAMPLES=1
TIME_TO_SLEEP=600


if [ ! -d $SOP_DIR/dependencies ]; then
{
	echo "wget -O ~ http://dependecies.sh"
}
fi


pushd $SOP_DIR

#sudo sh dependencies.sh

if [ $# -eq 4 ]; then
{
	TYPE=$1
	INTERFACE=$2
	DURATION=$3
	FILE_NAME=$4

	if [ $5 ]; then
        {
                $URL=$4
        }
        fi

        if [ $6 ]; then
        {
                $PORT=$5
        }
        fi

        if [ $7 ]; then
        {
                $CHANNEL=$4
        }
        fi

        if [ $8 ]; then
        {
                $IN_PORT=$4
        }
        fi

        if [ $9 ]; then
        {
                $OUT_PORT=$8
        }
        fi

}
else {
	echo "Use $0 NODE_TYPE INTERFACE DURATION FILE_NAME [URL] [PORT] [CHANNEL_ID] [IN_PORT] [OUT_PORT]"
	exit 2
}
fi

if [ -f sopcast.log ]; then
{
        sudo rm sopcast.log
}
fi

if [ "$TYPE" == "MONITOR" ]; then
{
	for i in $(seq 1 $NUM_SAMPLES)
	do
	{
		#sudo touch $RESULTS/$i.$FILE_NAME
		#echo "Escrevendo dump da placa $INTERFACE em $i.$FILE_NAME"
		$TIMEOUT $DURATION $SOP_EXE sop://$URL:$PORT/$CHANNEL $IN_PORT $OUT_PORT > sopcast.log
		#sudo $TSHARK -a duration:$(($DURATION+10)) -i $INTERFACE -n -F libpcap -w $RESULTS/`hostname`.$i.$FILE_NAME
		#sleep $TIME_TO_SLEEP
	}
	done
}
else {
	$SOP_EXE sop://$URL:$PORT/$CHANNEL $IN_PORT $OUT_PORT > sopcast.log
	#sudo $TSHARK -a duration:$(($DURATION+10)) -i $INTERFACE -n -F libpcap -w $RESULTS/$FILE_NAME

}
fi

#sh create_analisys.sh

#$TIMEOUT $DURATION $SOP_EXE sop://$URL:$PORT/$CHANNEL $IN_PORT $OUT_PORT >> /tmp/sopcast.log &
#$TIMEOUT $(($DURATION+20)) sudo $TSHARK -i $INTERFACE -n -aduration:$DURATION -F libpcap -w $SOP_DIR/$FILE_NAME

#/bin/sleep 60

#$TSHARK -n -F libpcap -r $SOP_DIR/$FILE_NAME -R "udp.port == $IN_PORT" -w $SOP_DIR/filtered.$FILE_NAME

popd
