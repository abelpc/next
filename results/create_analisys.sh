#!/bin/bash

SCRIPT=`pwd`/analisys/anv2.py
RESULTS_DIR=`pwd`/results
FINAL_RESULT=`pwd`/results
SAMPLES=samples/

if [ ! -d $RESULTS_DIR ]; then
{
	mkdir $RESULTS_DIR
}
fi

sudo chown rnp_OSN $RESULTS_DIR

#pushd ~/sopcast

IPS=(`sh get_ip.sh`)

if [ -d $SAMPLES ]; then
{
	pushd $SAMPLES

		i=0

		for y in `ls`; do
		{
			MY_IP=`../get_ip.sh`
			echo "Criando arquivo de estatísticas para amostra $y ($MY_IP)"
	        	if [ ! `du $y | awk '{print $1}'` -eq 0 ]; then
	        	{
				sudo $SCRIPT $y $MY_IP | sort -k8 -r > $RESULTS_DIR/$y.stats
				i=$(($i + 1))
			}
			fi
		}
		done

		popd
}
else {
	echo "$SAMPLES was not found"
}
fi

#popd
