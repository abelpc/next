
class Pacote:
	'Common base class for all the packets analyzed by the Analyzer v1'

	#src_calls = 0
	dst_calls = 0
	percent = 0

	def __init__(self, src_ip, src_pt, dst_ip, dst_pt):

		self.src_ip = src_ip
		self.src_pt = src_pt
		self.dst_ip = dst_ip
		self.dst_pt = dst_pt
		#self.dst_calls = 1	# When you instantiate a Pacote's object 
					# we set the destination's number of calls to one <- Not sure yet

	# Getters and Setters

	#def set_src_call(self, src_calls):
	#	self.src_calls = src_calls

	def set_dst_call(self, dst_calls):
		self.dst_calls = dst_calls

	def set_src_pt(self, src_pt):
		self.src_pt = src_pt

	def set_dst_pt(self, dst_pt):
		self.dst_pt = dst_pt

	def set_percent(self, percent=0):
		self.percent = percent

	def get_src_ip(self):
		return self.src_ip

	def get_dst_ip(self):
		return self.dst_ip

	def get_percent(self):
		return self.percent

	# Utilities

	def inc_src_calls(self):
		self.src_calls = self.src_calls + 1

	def inc_dst_calls(self):
		self.dst_calls = self.dst_calls + 1

	def __repr__(self):
		return "Pacote(source_ip, source_port, destination_ip, destination_port)"

	def __str__(self):
		return "Source IP: %s:%s \t\t\t Destination IP: %s:%s \t\t %s \t %s%%" % (self.src_ip, self.src_pt, self.dst_ip, self.dst_pt, self.dst_calls, self.percent)
