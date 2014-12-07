#!/usr/bin/python

import subprocess
import xmlrpclib
api_server = xmlrpclib.ServerProxy('https://www.planet-lab.org/PLCAPI/', allow_none=True)

auth = {}
auth['AuthMethod'] = 'password'
auth['Username'] = 'abelpc_uff@yahoo.com.br'
auth['AuthString'] = 'dkwpq753'

#return_fields = ['node_ids']
return_fields = ['slice_id', 'node_ids']

my_nodes = api_server.GetSlices(auth, None, return_fields)

slice_id = my_nodes[0]['slice_id']

p = subprocess.Popen(['./teste2.sh'], stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE)
out, err = p.communicate()
#print out

i = 0
for host in out.split():
	#print hosts
	j = api_server.DeleteSliceFromNodes(auth, slice_id, [host])
	
	if j == 1:
		print "Host %s removido com sucesso" % (host)
		i = i + 1

print "%i foram removidos do slice %i" % (i, slice_id)
