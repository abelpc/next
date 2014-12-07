#!/bin/bash

counter=0

KEY=~/sopcast/planetlab-key
PLANET_USER="rnp_OSN"
MONITOR_COMMAND='sopcast/collect.sh 1'
NODE_COMMAND='sopcast/collect.sh'
#SSH_COMMAND
REMOTE_FILE_NAME="1.monitor.pcap"
REMOTE_FILE_DIR="/home/$PLANET_USER/sopcast/results"
REMOTE_FILE="$REMOTE_FILE_DIR/$REMOTE_FILE_NAME"

FIRST=10
LAST=50
GAP=10
INTERVALS=`seq -w $LAST $((-1 * $GAP)) $FIRST`

NODES=(`echo $(./list_nodes.py -)`)
#NODES=(`cat ../nodes_list.txt`)
MONITORS=(${NODES[@]:0:$FIRST})
#MONITORS=`echo $(./list_nodes.py -m $FIRST)`
TOTAL_NODES=${#NODES[@]}
TOTAL_MONITORS=${#MONITORS[@]}

echo "There are $TOTAL_MONITORS and $TOTAL_NODES nodes.."


if [ ! -d samples ]; then
{
	mkdir samples

	for samples in $INTERVALS; do
	{
		if [ ! -d samples/$samples ]; then
		{
			mkdir samples/$samples
		}
		fi
	}
	done
}
fi

#echo ${MONITORS[@]}

function contains() {
    local n=$#
    local value=${!n}
    for ((i=1;i < $#;i++)) {
        if [ "${!i}" == "${value}" ]; then
#            echo "y"
            return 1
        fi
    }
#    echo "n"
    return 0
}

for interval in $INTERVALS; do
{
	NODES_TEMP=()
	for temp_node in ${NODES[@]}; do
	{
		$(contains "${MONITORS[@]}" "$temp_node")
		value=$?

		if [ $value == 0 ]; then
		{
			NODES_TEMP=(${NODES_TEMP[@]} $temp_node)
		}
		else {
			echo "ITS A MONITOR"
		}
		fi
	}
	done

        #NODES_TEMP=(${NODES[@]:$FIRST:$interval})
        echo "Opening a swarm with ${#NODES_TEMP[@]} nodes..:"
	#echo ${NODES_TEMP[@]}
        
	#@read -n 1 abel
	#csshX -l $PLANET_USER -ssh_args "-i $KEY" ${NODES_TEMP[@]} --remote_command $NODE_COMMAND
	cssh -l $PLANET_USER -o "-i $KEY" ${NODES_TEMP[@]} -a $NODE_COMMAND
	sleep $interval

	for monitor in ${MONITORS[@]}; do
	{
		echo "Connecting $monitor to the swarm of interval# $interval ..."
		ssh -i "$KEY" -l $PLANET_USER $monitor "$MONITOR_COMMAND"

		if [ -f samples/$interval/$REMOTE_FILE_NAME ]; then
		{
			mv samples/$interval/$REMOTE_FILE_NAME samples/$interval/`date "+%Y%m%d-%Hh%M"`_$REMOTE_FILE_NAME
		}
		fi

		echo "Trying to get $REMOTE_FILE..."
		scp -i planetlab-key $PLANET_USER@$monitor:$REMOTE_FILE samples/$interval
		SCP_FILE=$?
		while [ $SCP_FILE -gt 0 ]; do
		{
			echo "Error getting $monitor/$REMOTE_FILE_NAME! Do you want to try again? (Y/n)"
			next="Y"
			read -n 1 next
			if [ "$next" == "Y" || "$next" == "y" ]; then
			{
				scp -i planetlab-key rnp_OSN@$monitor:$REMOTE_FILE samples/$interval
				SCP_FILE=$?
			}
			else {
				SCP_FILE=0
			}
			fi
		}
		done

		mv -v samples/$interval/$REMOTE_FILE_NAME samples/$interval/$monitor.$REMOTE_FILE_NAME
		echo "['#'$monitor] Fineshed with $monitor"
	}
	done

	echo "Fineshed with interval# $interval. Sleeping for a minute."
	sleep 60
	echo "Killing all processes that we started..."
	killall ssh
	killall csshX
	echo "Restart the SopCast server and press [ENTER] to continue."
	read -n 1 next
}
done

echo "Finished! Exiting..."

: '
ssh -i planetlab-key rnp_OSN@$MONITOR 'sh ~/sopcast/collect.sh 1; sudo chown -R rnp_OSN /home/rnp_OSN/sopcast/results' &
csshX -l rnp_OSN --ssh_args '-i planetlab-key' `echo $(./list_nodes.py - 50)` --remote_command sopcast/collect.sh
sleep $((200 + (60*10*10) + 120))
killall csshX
killall ssh

#scp -i planetlab-key rnp_OSN@$MONITOR:~/sopcast/{5min.pcap,10min.pcap,20min.pcap} samples/50
scp -r -i planetlab-key rnp_OSN@$MONITOR:~/sopcast/results samples/50

for x in `ls samples/50/results`; do
{
	mv -v samples/50/results/$x samples/50
}
done

if [ $? != 0 ]; then
{
	echo "Erro com $x"
}
fi

echo "Finished for 50 nodes. Exiting..."
:
