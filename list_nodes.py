#!/usr/bin/python

import sys
import xmlrpclib

api_server = xmlrpclib.ServerProxy('https://www.planet-lab.org/PLCAPI/', allow_none=True)

auth = {}
auth['AuthMethod'] = 'password'
auth['Username'] = 'user@email.com'
auth['AuthString'] = 'password'

#authorized = api_server.AuthCheck(auth)

#return_fields = ['node_ids']
return_fields = ['slice_id', 'node_ids']

my_nodes = api_server.GetSlices(auth, None, return_fields)
#print my_nodes[0]['node_ids']

hosts = api_server.GetNodes(auth, my_nodes[0]['node_ids'], ['hostname'])

#print sys.argv[1:]

list = ''

num_hosts = len(hosts)
i = None


if (len(sys.argv) >= 3):
	i = int(sys.argv[2])


if sys.argv[1:][0] == "-m":
	for num in range (0, i):
		list += "%s " % hosts[num]['hostname']
	#print hosts[0]['hostname']

else:
	if i == None:
		for num in range (0, num_hosts):
			list += "%s " % hosts[num]['hostname']
	else:
		for num in range (i+1, num_hosts):
			list += "%s " % hosts[num]['hostname']

print list
