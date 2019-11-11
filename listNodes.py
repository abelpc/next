#!/usr/bin/python

import sys
import xmlrpclib

class listNodes:

	api_server = xmlrpclib.ServerProxy('https://www.planet-lab.org/PLCAPI/', allow_none=True)
	slice_name = None
	
	auth = {}
	private_key = 'sopcast/planetlab-key'

	return_fields = ['slice_id', 'node_ids']

	my_nodes = ''

	def __init__(self):
		#return_fields = ['node_ids']
		self.return_fields = ['slice_id', 'node_ids']

	def authenticate(self, user, password):
		self.auth['AuthMethod'] = 'password'
		self.auth['Username'] = user
		self.auth['AuthString'] = password
		
		try:
			authorized = self.api_server.AuthCheck(self.auth)
			
		except:
			authorized = False
		
		return authorized

	def setPrivateKey(self, private):
		self.private_key = private

	def getPrivateKey(self):
		return self.private_key

	def getUser(self):
		return self.auth['Username']

	def getSliceName(self):
	
		if self.slice_name == None:
			self.slice_name = self.api_server.GetSlices(self.auth, None, ['name'])
		#slice_username = self.api_server.GetPersons(self.auth, None, None)
		return self.slice_name[0]['name']

	def getNodes(self):
		nodes = []
		
		nodes = self.api_server.GetNodes(self.auth, None, ['boot_state', 'site_id', 'hostname', 'node_id'])
		
		return nodes


	def getSlices(self):

		hosts = []

		self.my_nodes = self.api_server.GetSlices(self.auth, None, self.return_fields)
		#print my_nodes[0]['node_ids']

		hosts = self.api_server.GetNodes(self.auth, self.my_nodes[0]['node_ids'], ['node_id', 'hostname'])

		return hosts

		#print sys.argv[1:]


		#list = ''

		#i = len(hosts)

		#for num in range (0, i):
		#	list += "%s " % hosts[num]['hostname']
