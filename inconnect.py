import urllib2

class Connect:

	planetlab_ip = 'http://128.112.139.90'
		
	def check_connectivity(self):
		self.check_connectivity(self, self.planetlab_ip)

	def check_connectivity(self, reference=None, time_out=None):

		if reference == None:
			reference = self.planetlab_ip
			
		if time_out == None:
			time_out = 5

		try:
			urllib2.urlopen(reference, timeout=time_out)
			return True

		except:
			return False
