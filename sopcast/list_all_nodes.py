#!/usr/bin/python

import sys
import xmlrpclib

api_server = xmlrpclib.ServerProxy('https://www.planet-lab.org/PLCAPI/', allow_none=True)

auth = {}
auth['AuthMethod'] = 'password'
auth['Username'] = 'abelpc_uff@yahoo.com.br'
auth['AuthString'] = 'dkwpq753'

#authorized = api_server.AuthCheck(auth)

#return_fields = ['node_ids']
return_fields = ['slice_id', 'node_ids']

my_nodes = api_server.GetSlices(auth, None, return_fields)
#print my_nodes[0]['node_ids']

hosts = api_server.GetNodes(auth, my_nodes[0]['node_ids'], ['hostname'])

#print sys.argv[1:]

list = ''

i = len(hosts)

if (len(sys.argv) >= 3):
	i = int(sys.argv[2])

if sys.argv[1:][0] == "-l":

	for num in range (0, i):
		list += "%s " % hosts[num]['hostname']

	print list
else:
	for num in range (0, i):
		print hosts[num]['hostname']
