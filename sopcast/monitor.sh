#!/bin/bash

INTERFACE=eth0
SCRIPT=~/sopcast/sampler.sh

echo "Running as a Monitor for 10 seconds"

sudo sh $SCRIPT "MONITOR" $INTERFACE 10 monitor.pcap

sleep 55

echo "Exiting..."
