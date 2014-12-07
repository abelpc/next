#!/bin/bash

for x in $(../list_nodes.py -); do
{
        IP=`../samples/get_ip.sh $x`
	
	if [ "$IP" != "" ]; then
	{
		echo $IP
	}
	fi
}
done
