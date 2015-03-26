#!/bin/bash

SSH_KEY=$1
USERNAME=$2

for x in $(./list_nodes.py -); do
	if [ $? == "200" ]; then
	{
		echo "Skipping $x.."
	}

	else {
		echo "Sending and Installing dependencies on $x..."
		#scp -r {dependencies,sp-auth} -i planetlab-key rnp_OSN@$x:~/sopcast
		scp sopcast/dependencies.sh -i $SSH_KEY $USERNAME@$x:~/
		ssh -i $SSH_KEY $USERNAME@$x 'sh ~/dependencies.sh' 
	}
	fi
done
