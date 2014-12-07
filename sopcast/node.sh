#!/bin/bash

INTERFACE=eth0
SCRIPT=~/sopcast/sampler.sh

echo "Running as a Node for 1200 seconds"

sudo sh $SCRIPT "NODE" $INTERFACE 1200 node.pcap

echo "Exiting..."
