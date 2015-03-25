#!/bin/bash

HOME_DIR="/home/$USER"
SOP_DIR=$HOME_DIR/sopcast
DEPENDENCIES=$SOP_DIR/dependencies
TSHARK="/usr/sbin/tshark"

if [ ! -d $SOP_DIR ]; then
{
        #copy_result=`cp -av /tmp/sopcast ~`

        if [ ! -d $SOP_DIR ]; then
        {
                mkdir $SOP_DIR
        }
        fi
}
fi

pushd $SOP_DIR

if [ ! -d $DEPENDENCIES ]; then
{
	mkdir dependencies
}
fi

if [ ! -d $SOP_DIR/results ]; then
{
        mkdir results
}
fi

if [ ! -d $SOP_DIR/sp-auth ]; then
{
        wget -O $DEPENDENCIES/sp-auth.tgz http://download.sopcast.com/download/sp-auth.tgz
        tar -xvzf $DEPENDENCIES/sp-auth.tgz -C $SOP_DIR
}
fi

if [ ! -f $TSHARK ]; then
{
        sudo yum -y --nogpgcheck install wireshark
}
fi

if [ ! -f /usr/lib/libstdc++.so.5 ]; then
{
        if [ ! -f $DEPENDENCIES/libstdcpp5.tgz ]; then
        {
                wget --no-check-certificate -O $DEPENDENCIES/libstdcpp5.tgz http://www.sopcast.com/download/libstdcpp5.tgz
        }
	fi
	
	tar -xvzf $DEPENDENCIES/libstdcpp5.tgz -C $DEPENDENCIES
        sudo cp -av $DEPENDENCIES/usr/lib/libstdc++.so.5 /usr/lib/
        sudo cp -av $DEPENDENCIES/usr/lib/libstdc++.so.5.0.1 /usr/lib
}
fi

pushd $DEPENDENCIES

sudo yum -y --nogpgcheck install unzip libpcap-devel libpcap gcc-c++ gcc bind-utils

if [ -f impacket-0.9.12.tar.gz ]; then
{
	IMPACKET_FILE="impacket-0.9.12.tar.gz"
}
else {
	wget --no-check-certificate https://pypi.python.org/packages/source/i/impacket/impacket-0.9.12.tar.gz

	if [ $? != 0 ]; then
	{
		if [ -f impacket-0.9.11.tar.gz ]; then
		{
			IMPACKET_FILE="impacket-0.9.11.tar.gz"
		}
		else {
			wget --no-check-certificate https://pypi.python.org/packages/source/i/impacket/impacket-0.9.11.tar.gz

			if [ $? != 0 ]; then
			{
				echo "It was not possible to download Impacket. Please, download version 0.9.11 or 0.9.12 to $DEPENDENCIES directory."
				exit 3
			}
			else {
				IMPACKET_FILE="impacket-0.9.11.tar.gz"
			}
			fi
		}
		fi
	}
	else {
		IMPACKET_FILE="impacket-0.9.12.tar.gz"
	}
	fi
}
fi

tar -xvzf $IMPACKET_FILE
pushd `echo $IMPACKET_FILE | awk -F '.tar.gz' '{print $1}'`
sudo python setup.py install 
popd # Exiting impacket directory

PCAP_FILE="pcapy-0.10.8.zip"

if [ ! -f $PCAP_FILE ]; then
{
	echo "It was not possible to download Pcapy.
 Please, download version 0.10.8 to $DEPENDENCIES directory."
	exit 4
}
fi
unzip -o pcapy-0.10.8.zip 
pushd pcapy-0.10.8 
sudo python setup.py install
popd # Exiting pcapy directory

popd # Exiting dependencies directory

popd # Exiting sopcast directory

