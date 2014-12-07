#!/bin/bash



DIR=$1

#for x in `ls $DIR`; do
#{
#	ip=`sh ../samples/get_ip.sh $x`
#	echo $ip
#}
#done

for x in `ls $DIR`; do
{
	ip=`sh ../samples/get_ip.sh $x`
	if [ "$ip" != "" ]; then
	{
		python anv2.py "$DIR/$x" $ip > generate_stats/$ip.stats
	}
	else {
		echo "$x could not be resolved."
	}
	fi
}
done
