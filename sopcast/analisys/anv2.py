#!/usr/bin/python

import sys
from pcapy import open_offline
import impacket
from impacket import ImpactPacket
from impacket.ImpactDecoder import EthDecoder
from impacket.ImpactPacket import IP, TCP, UDP, ICMP
from Pacote import *
 
temp = {}
#pcap = open_offline("tcpdump.pcap")
pcap_file = sys.argv[1]
pcap = open_offline(pcap_file)
decoder = EthDecoder()
#my_ip = "192.168.1.9"
my_ip = sys.argv[2]
global first_pack_timestamp
first_pack_timestamp = None 
global num_packs
num_packs = 1
num_ips = 0

def callback(hdr, data):
	#print hdr.getts()[0]
	global first_pack_timestamp 
	if (first_pack_timestamp == None):
		#first_pack_timestamp = (hdr.getts()[0] * (10**(-6))) + hdr.getts()[1] #hdr.getts()[1] * (10**(-6))
		first_pack_timestamp = hdr.getts()[0]

	#timestamp = hdr.getts()[1] * (10**(-6))
	#timestamp = (hdr.getts()[0] * (10**(-6))) + hdr.getts()[1]
	timestamp = hdr.getts()[0]	

	delta_time = timestamp - first_pack_timestamp
	#print "[%i] %f - %f = %f" % (num_packs, timestamp, first_pack_timestamp, delta_time )

	global num_packs
	global num_ips

	if num_ips <= 4:
		#print "callback()"
		packet=decoder.decode(data)
		l2=packet.child()

		if isinstance(l2, IP):
			#print "IP",
			l3=l2.child()
			src_ip = l2.get_ip_src()
			dst_ip = l2.get_ip_dst()

			if isinstance(l3, TCP):
				src_port = l3.get_th_sport()
				dst_port = l3.get_th_dport()
            
			else:
				if isinstance(l3, UDP):
					#print "UDP"
					src_port = l2.child().get_uh_sport()
					dst_port = l2.child().get_uh_dport()

				else:
					#print "Breaking!"
					return

			#print "Packet from %s (%s) to %s(%s) " % (src_ip, src_port, dst_ip, dst_port)

			if ((src_port == 3908) and (src_ip == my_ip)):			
			#if ((src_port == 3908) and (src_ip == my_ip) and (dst_port == 3908)):			
				num_packs = num_packs + 1

				if not (temp.has_key(src_ip)):
					tmp_packet = Pacote(src_ip, src_port, dst_ip, dst_port)
					tmp_packet.inc_dst_calls()
					#temp[src_ip] = tmp_packet
					temp[dst_ip] = tmp_packet

					#num_ips = num_ips + 1 # Increment the number of gotten IPs

				else:
					tmp_packet = temp[dst_ip]
					tmp_packet.inc_dst_calls()	# Increment the source's number of destination calls
					temp[dst_ip] = tmp_packet	# Saves the incrementation

					#if not (temp.has_key(dst_ip)):	# Counting the opposite direction, but not necessary
					#	tmp_packet = Pacote(dst_ip, dst_port, src_ip, src_port)
					#	temp[dst_ip] = tmp_packet

					#tmp_packet = temp[dst_ip]
					#tmp_packet.inc_dst_calls()	# Increment the destination's number of destination calls
									# Notice that this number represents different things for the 
									# viewer IP and for all the other sources
					#temp[dst_ip] = tmp_packet

				#print "UDP from %s (%s) to %s(%s) " % (src_ip, dst_port, dst_ip, src_port)
		

def percent(total, z):
	if z == 0:
		return -1
	return ((float)(100 * z)/num_packs)

pcap.loop(0, callback)

for x in temp.keys():
	if (x != my_ip):
		#print '#### First Analisys... ####'
		tmp_packet = temp[x]
		#print temp[my_ip].dst_calls
		#print temp[x].dst_calls
		#print "my_ip = %s e x = %s" % (my_ip, x) 
		#tmp_packet.set_percent(percent(temp[my_ip].dst_calls, temp[x].dst_calls)) # Setting the percentage
		#tmp_packet.set_percent(percent(num_packs, temp[x].dst_calls)) # Setting the percentage
		#print temp[x]
		print x

one = {}
one = temp
# Time to save 'one' in a file, right?
	
# Doing everything again for the second file...
#temp = {}
#pcap = open_offline("libcap2.pcap")
#pcap.loop(0, callback)

#print ' '
#print '###########################################################'
#print ' '

#for x in temp.keys():
#	print '#### Second Analisys... ####
#	tmp_packet = temp[x]
#	#print temp[my_ip].dst_calls
	#print temp[x].dst_calls
#	tmp_packet.set_percent(percent(temp[my_ip].dst_calls, temp[x].dst_calls)) # Setting the percentage
#	print temp[x]

#print "Done"
