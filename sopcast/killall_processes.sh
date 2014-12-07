#!/bin/bash

counter=0
for x in $(./list_all_nodes.py -); do
	ssh -i planetlab-key rnp_OSN@$x 'sudo killall collect.sh tshark; sleep 1; exit 1>/dev/null 2>&1' 1>/dev/null 2>&1
	if [ $? != 0 ]; then {
		echo "[ERRO] em $x"
		let counter=counter+1
	}
	fi
done


echo "Total de Hosts com erro: $counter"
