#!/bin/bash

GET_IP=../../get_ip.sh
NODES_DIR=joined/

pushd $NODES_DIR

if [ ! -d ips ]; then
{
	mkdir ips
}
fi

for x in `ls`; do
{
	if [ ! -d $x ]; then
	{
		ip=`$GET_IP $x`
		cp -av $x ips/$ip.stats
	}
	fi
}
done

popd
