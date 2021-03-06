# Files and Directories
import os

# GTK
from gi.repository import Gtk, GLib

# Our Stuff
from listNodes import *
from inconnect import *

import subprocess

# SSH & SCP
import paramiko
import scpclient
from contextlib import closing

# Thread Support
import threading
import sys
import time


outlock = threading.Lock()

class Dialog ():

	total_sent = 0
	total_received = 0
	connection = None
	msgDialog = None
	online = 0
	offline = 0
	total_nodes = 0
	total_monitors = 0
	
	workDirContent = None
	workDirPath = None
	node_remoteCmd = None
	node_kill = None
	monitor_remoteCmd = None
	monitor_kill = None
	lock = None
	
	ssh_nodes = []
	ssh_monitors = []

	def __init__(self, builder, win=None, connection=None):

		self.builder = builder
		
		if self.connection == None:
			self.connection = listNodes()
		else:
			self.connection = connection

		if (win == "mainDialog"):
			self.mainDialog_name = win
			self.mainDialog()
		if (win == "addDlg"):
			self.addDialog_name = win
			self.addDialog()
			
	def addDialog(self):
		self.addDlg = self.builder.get_object(self.addDialog_name)
		self.addDlg.show()
		
		planet_api = listNodes()
		
		treeview = self.builder.get_object("add_treeview")
			
		nodes = planet_api.getNodes()
		i = len(nodes)
		
		nodeList = Gtk.ListStore(bool, str, str, int, int)
		
		node_toggle = Gtk.CellRendererToggle()
		node_toggle.connect("toggled", self.on_cell_toggled)
		column_toggle = Gtk.TreeViewColumn('', node_toggle, active=0)
		treeview.append_column(column_toggle)
		
		state_column = Gtk.TreeViewColumn("Boot State", Gtk.CellRendererText(), text=1)
		state_column.set_resizable(True)
		state_column.set_sort_column_id(1)
		treeview.append_column(state_column)
		
		hostname_column = Gtk.TreeViewColumn("Hostname", Gtk.CellRendererText(), text=2)
		hostname_column.set_resizable(True)
		hostname_column.set_sort_column_id(2)
		treeview.append_column(hostname_column)
		
		siteid_column = Gtk.TreeViewColumn("Site ID", Gtk.CellRendererText(), text=3)
		siteid_column.set_resizable(True)
		siteid_column.set_sort_column_id(3)
		treeview.append_column(siteid_column)
		
		nodeid_column = Gtk.TreeViewColumn("Node ID", Gtk.CellRendererText(), text=4)
		nodeid_column.set_resizable(True)
		nodeid_column.set_sort_column_id(4)
		treeview.append_column(nodeid_column)
		
		treeview.set_model(nodeList)
		treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
		#print dir(treeview)
		#treeview.TreeSelection.set_mode(Gtk.SelectionMode.MULTIPLE)

		for num in range(0, i):
			nodeList.append([False, nodes[num]['boot_state'], nodes[num]['hostname'], nodes[num]['site_id'], nodes[num]['node_id']])		

		self.show_message_dlg("Lista Carregada com sucesso!", Gtk.MessageType.INFO, "Information")

	def mainDialog(self):
	
		window2 = self.builder.get_object(self.mainDialog_name)
		window2.show()
		#window = threading.Thread(target=window2.show)
		#window.start()
		#window.join()

		treeview = self.builder.get_object("nodeview")
		self.statusbar = self.builder.get_object("statusbar1")

		save_menu = self.builder.get_object("imagemenuitem3")
		save_menu.connect('activate', self.on_save_menu_file)

		selAllBt = self.builder.get_object("selectallBt")
		selAllBt.connect('clicked', self.selAllclicked)
		selBt_menu = self.builder.get_object("select_menu")
		selAllBt.set_menu(selBt_menu)
		
		startBt = self.builder.get_object("start_button")
		startBt.connect('clicked', self.start)
		
		pkChooser = self.builder.get_object("pkchooserBt")
		pkChooser.connect('file-set', self.pkset)
		
		fileChooser = self.builder.get_object("filechooserdir")
		fileChooser.connect('file-set', self.fileset)
		
		refreshBt = self.builder.get_object("refreshbt")
		refreshBt.connect('clicked', self.refresh)

		sendDirBt = self.builder.get_object("sendDirBt")
		sendDirBt.connect('clicked', self.sendDir)

		user = self.connection.getUser()
		self.nodes_file = os.path.abspath(os.path.join('..', user, 'nodes_list.txt'))
		
		self.dirview()

		self.store = Gtk.ListStore(int, str, bool, bool, str, str)
		self.selectAll = Gtk.CheckButton()

		id_column = Gtk.TreeViewColumn("ID", Gtk.CellRendererText(), text=0)
		id_column.set_resizable(True)
		id_column.set_sort_column_id(0)
		treeview.append_column(id_column)

		host_column = Gtk.TreeViewColumn("Hostname", Gtk.CellRendererText(), text=1)
		host_column.set_resizable(True)
		host_column.set_sort_column_id(1)
		treeview.append_column(host_column)

		#node_toggle.connect("changed", self.on_tree_selection_changed)

		#column_toggle = Gtk.TreeViewColumn()
		#column_toggle.set_clickable(True)
		#column_toggle.add_attribute(renderer_toggle, "", 0)
				
		node_toggle = Gtk.CellRendererToggle()
		node_toggle.connect("toggled", self.on_cell_toggled)
		column_toggle = Gtk.TreeViewColumn("Node", node_toggle, active=2)
		treeview.append_column(column_toggle)
		
		status_toggle = Gtk.CellRendererToggle()
		status_toggle.connect("toggled", self.on_cell_status_toggled)
		status_column_toggle = Gtk.TreeViewColumn("Monitor", status_toggle, active=3)
		treeview.append_column(status_column_toggle)
		
		renderer_pixbuf = Gtk.CellRendererPixbuf()
		column_pixbuf = Gtk.TreeViewColumn("Status", renderer_pixbuf, stock_id=4)
		treeview.append_column(column_pixbuf)
		
		con_column = Gtk.TreeViewColumn("Connection", Gtk.CellRendererText(), text=5)
		con_column.set_resizable(True)
		con_column.set_sort_column_id(5)
		treeview.append_column(con_column)

		treeview.set_model(self.store)
		treeview.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)
		#print dir(treeview)
		#treeview.TreeSelection.set_mode(Gtk.SelectionMode.MULTIPLE)

		host_icon_status = Gtk.STOCK_DIALOG_QUESTION
		host_threads = []
		
		if os.path.exists(self.nodes_file):
			answer = self.show_message_dlg("A configuration file was found on your local directory. Do you want to load nodes and configurations from this file?", Gtk.MessageType.QUESTION)
			if (answer == Gtk.ResponseType.YES):
				f = open(self.nodes_file, 'r')
				
				for line in f:
					attributes = line.split()
					node_id = attributes[0]
					hostname = attributes[1]
					
					if attributes[2] == 'False':
						node_node = 0
					else:
						node_node = 1
						self.total_nodes = self.total_nodes + 1
					if attributes[3] == 'False':
						node_monitor = 0
					else:
						node_monitor = 1
						self.total_monitors = self.total_monitors + 1
					
					self.store.append([int(node_id), hostname, node_node, node_monitor, Gtk.STOCK_DIALOG_QUESTION, "Disconnected"])
					
				self.statusbar.push(self.online, ("Click on 'Check Status' to check the status of each node on the list."))
				
	def pkset(self, widget):
		f = widget.get_filename()
		self.connection.setPrivateKey(f)			
		
	
	def sendDir(self, widget):
		total_sent = 0	

		(connected_nodes, disconnected_nodes) = self.get_nodes("nodes")
		(connected_monitors, disconnected_monitors) = self.get_nodes("monitor")
		
		i = len(disconnected_nodes)
		j = len(disconnected_monitors)
		l = len(connected_nodes)
		m = len(connected_monitors)
		
		if l + m == 0:
			self.show_message_dlg("Please, select at least one node and/or one monitor.", Gtk.MessageType.INFO, "Select some host")
			return False
			
		if self.workDirPath == None:
			self.show_message_dlg("Please, select a working directory.")
			return False
			
		if self.connection.getPrivateKey() == None:
			self.show_message_dlg("Please, select a private-key.")
			return False
		
		if ((i > 0) or (j > 0)):
			answer = self.show_message_dlg("There are %d offline nodes which will not establish a connection. Do you want to continue without them?" % (i + j), Gtk.MessageType.QUESTION, "Offline Nodes")
			if (answer == Gtk.ResponseType.YES):
				(self.ssh_nodes, self.ssh_monitors) = self.connect(connected_nodes, connected_monitors)
				
		else:
			(self.ssh_nodes, self.ssh_monitors) = self.connect(connected_nodes, connected_monitors)
		
		self.set_statusbar("Sending files...")
		self.total_sent = 0
		#total_ssh_nodes = len(connecte)
		
		for ssh in range(0, l):
			host_t = threading.Thread(target=self.scp_send, args=(self.workDirPath, self.ssh_nodes[ssh],))
			host_t.start()
			
		for ssh in range(0, m):
			host_t = threading.Thread(target=self.scp_send, args=(self.workDirPath, self.ssh_monitors[ssh],))
			host_t.start()
				
		while (self.total_sent != (len(self.ssh_nodes) + len(self.ssh_monitors))):
			#print ("while..!")
			Gtk.main_iteration()
			self.set_statusbar("Sending file %i of %i..." % (self.total_sent, len(self.ssh_nodes) + len(self.ssh_monitors)))
		
		self.set_statusbar("Successfully sent files to %i nodes with %i errors" % (self.total_sent, l - self.total_sent))
		
				
	def scp_send (self, filename, ssh):
	
		#Gtk.main_iteration()
		#print ('/home/' + self.connection.getSliceName())
		try:
			with closing(scpclient.WriteDir(ssh.get_transport(), '/home/' + self.connection.getSliceName())) as scp:
				scp.send_dir(filename, preserve_times=True)
			self.total_sent = self.total_sent + 1
		except:
			self.set_statusbar("Error in one file...")
			
	def scp_get (self, ssh, filename):
	
		dirname = os.path.dirname(filename)
		filename = os.path.basename(filename)
		#print(dirname+filename)
		#Gtk.main_iteration()
		#print ('/home/' + self.connection.getSliceName())
		print("Downloading remote file %s..." % filename)
		self.ssh_cmd(ssh, str('killall -9 -w ' + self.node_kill + ' ' + self.monitor_kill))

		try:
			with closing(scpclient.Read(ssh.get_transport(), dirname)) as scp:
				final = scp.receive(filename)
				print (final)
			self.total_received = self.total_received + 1
		except:
			print ("Error in one file")
			self.set_statusbar("Error in one file...")

	def scp_os_get (self, ssh, filename, dest=None):
	
		dirname = os.path.dirname(filename)
		filename = os.path.basename(filename)
		
		fullpath = ssh + ':' + dirname + '/' + filename
		print ("Downloading remote file: %s" % fullpath)
		
		self.ssh_os_cmd(ssh, str('sudo killall -I -w -s 9 ' + self.node_kill + ' sp-sc-auth ' + self.monitor_kill))
		time.sleep(10)
		p = subprocess.Popen(['/usr/bin/scp', '-i', self.connection.getPrivateKey(), '-o ConnectTimeout=10', '-o User=' + self.connection.getSliceName(), fullpath, 'results/'+dest+'/'], stdout=subprocess.PIPE)
		#files, err = p.communicate()
		self.total_received = self.total_received + 1

	def ssh_os_cmd(self, ssh, cmd):
		p = subprocess.Popen(['/usr/bin/ssh', '-i', self.connection.getPrivateKey(), '-l', self.connection.getSliceName(), ssh, cmd], stdout=subprocess.PIPE)
		files, err = p.communicate()
		#files = files.splitlines()
		self.lock = False
		

	def ssh_cmd (self, ssh, cmd, lock=False):
	
		print("Trying to execute %s" % cmd)
	
		#channel = ssh.get_transport().open_session()
		#channel.setblocking(1)
		#channel.get_pty()

		#try:
		#channel.exec_command(str(cmd))
			
		stdin, stdout, stderr = ssh.exec_command(cmd, get_pty=True)

			
		if lock:
			#print("%s = %s" % (cmd, channel.recv_exit_status()))
			#print("leaving..")
			exit_status = stdout.channel.recv_exit_status()
			#while not stdout.channel.exit_status_ready():
			#	pass
			print (exit_status)
			self.lock = False

		self.total_sent = self.total_sent + 1
			
		#except:
		#	print ("Error executing SSH cmd in one node...")
		#	self.set_statusbar("Error executing in one host")
		#	self.total_sent = self.total_sent + 1
			
	def refresh (self, widget, nodes=None):
	
		if self.connection.getPrivateKey() == None:
			self.show_message_dlg("Please, select a private-key.")
			return False
			
		self.store.clear()
		self.total_nodes = 0
		self.total_monitors = 0
		
		if nodes == None:
			nodes = self.connection.getSlices()
			
		self.connection.getSliceName()
		self.addCheck_node(nodes)
	
	def fileset (self, widget):
		
		self.workDirContent.clear()
		self.workDirPath = widget.get_filename()
		
		for f in os.listdir(self.workDirPath):
			size = str(os.path.getsize(os.path.join(self.workDirPath, f)) / 1024)
			
			if os.path.isdir(os.path.join(self.workDirPath, f)):
				self.workDirContent.append([Gtk.STOCK_DIRECTORY, f, False, False, size])
			else:
				self.workDirContent.append([Gtk.STOCK_FILE, f, False, False, size])
	
	def start (self, widget):
		(connected_nodes, disconnected_nodes) = self.get_nodes("nodes")
		(connected_monitors, disconnected_monitors) = self.get_nodes("monitor")
		
		i = len(disconnected_nodes)
		j = len(disconnected_monitors)
		l = len(connected_nodes)
		m = len(connected_monitors)
		
		if l + m == 0:
			self.show_message_dlg("Please, select at least one node and/or one monitor.", Gtk.MessageType.INFO, "Select some host")
			return False
			
		if (self.node_remoteCmd == None and l != 0):
			self.show_message_dlg("Please, select a command to be executed on the nodes.")
			return False
			
		if (self.monitor_remoteCmd == None and m !=0):
			self.show_message_dlg("Please, select a command to be executed on the monitors.")
			return False
		
		if ((i > 0) or (j > 0)):
			answer = self.show_message_dlg("There are %d offline nodes which will not establish a connection. Do you want to continue without them?" % (i + j), Gtk.MessageType.QUESTION, "Offline Nodes")
			
			if (answer == Gtk.ResponseType.YES):
				(self.ssh_nodes, self.ssh_monitors) = self.connect(connected_nodes, connected_monitors)
		else:
			(self.ssh_nodes, self.ssh_monitors) = self.connect(connected_nodes, connected_monitors)
			
		self.total_sent = 0
		
		for ssh in range(0, l):
			host_t = threading.Thread(target=self.ssh_cmd, args=(self.ssh_nodes[ssh], self.node_remoteCmd,))
			host_t.start()
				
		while self.total_sent != len(self.ssh_nodes):
			#print ("while..!")
			Gtk.main_iteration()
			self.set_statusbar("Node's command execution... (%i of %i)" % (self.total_sent, len(self.ssh_nodes)))
			
		total_executed = 0
		monitors_threads = []

		for ssh in range(0, m):
			self.lock = True
			self.total_sent = 0
			connection = connected_monitors[ssh]
			print (connection)
			monitor_t = threading.Thread(target=self.ssh_os_cmd, args=(connection, self.monitor_remoteCmd,))
			monitor_t.start()
			#monitor_t.join()
			monitors_threads.append(monitor_t)
			
			total_executed = total_executed + 1
			#while self.total_sent != 1:
			while self.lock:
				self.set_statusbar("Monitor's command execution... (%i of %i)" % (total_executed, m))
				Gtk.main_iteration()
		
		for ssh in range(0, m):
			#p = subprocess.Popen(['/bin/bash', 'get_ip.sh', connected_monitors[ssh]], stdout=subprocess.PIPE)
			#files, err = p.communicate()
			#files = files.splitlines()
			ip = connected_monitors[ssh]
			
			dirname = os.path.basename(self.workDirPath)
			fullpath = '/home/' + self.connection.getSliceName() + '/' + dirname + '/results/' + connected_monitors[ssh] + '.pcap.stats'
			
			monitors_t = threading.Thread(target=self.scp_os_get, args=(connected_monitors[ssh], fullpath, 'monitors',))
			monitors_t.start()
			
		while self.total_received != len(self.ssh_monitors):
			#print ("while..!")
			Gtk.main_iteration()
			self.set_statusbar("Getting file number %i from monitor %s..." % (self.total_received, ip))
			
		self.total_received = 0	
		
		for ssh in range(0, l):
			#p = subprocess.Popen(['/bin/bash', 'get_ip.sh', connected_nodes[ssh]], stdout=subprocess.PIPE)
			#files, err = p.communicate()
			#files = files.splitlines()
			#ip = files[0]
			ip = connected_nodes[ssh]
	
			dirname = os.path.basename(self.workDirPath)
			fullpath = '/home/' + self.connection.getSliceName() + '/' + dirname + '/results/' + connected_nodes[ssh] + '.pcap.stats'
			nodes_t = threading.Thread(target=self.scp_os_get, args=(connected_nodes[ssh], fullpath, 'nodes',))
			nodes_t.start()
			
		while self.total_received != len(self.ssh_monitors):
			#print ("while..!")
			Gtk.main_iteration()
			self.set_statusbar("Getting file number %i from monitor %s..." % (self.total_received, ip))
			
		self.set_statusbar("Finished execution. Opening results' dir and closing remaining connections.")
		p = subprocess.Popen(['/usr/bin/pcmanfm', 'results'], stdout=subprocess.PIPE)
		
		for ssh in range(0, l):
			#p = subprocess.Popen(['/bin/bash', 'get_ip.sh', connected_nodes[ssh]], stdout=subprocess.PIPE)
			#files, err = p.communicate()
			#files = files.splitlines()
			#ip = files[0]
			#ip = connected_nodes[ssh]

			nodes_t = threading.Thread(target=self.ssh_os_cmd, args=(connected_nodes[ssh], str('sudo killall -I -w -s 9 sp-sc-auth'),))
			nodes_t.start()
			
	def close_ssh_connections (self):
	
		total_nodes = len(self.ssh_nodes)
		total_monitors = len(self.ssh_monitors)
		
		for node in range(0, total_nodes):
			self.ssh_nodes[node].close()
		
		for monitor in range(0, total_monitors):
			self.ssh_monitors[monitor].close()
			
		self.set_statusbar("%i connections closed." % (total_nodes + total_monitors))
			
	def host_path_lookup (self, host):
		i = len(self.store)
		
		for num in range(0, i):
			node = self.store[num]
			
			if node[1] == host:
				return num
				
		return None		
	
	def connect (self, nodes, monitors, intervals=None):
		ssh_nodes = []
		ssh_monitors = []
		host_threads = []
		
		if intervals == None:
			intervals = {len(nodes)}

		for interval in intervals:
			
			if interval > len(nodes):
				interval = len(nodes)
			# Connecting nodes (Forming a swarm)
			for node in range(0, interval):
				print ("SSHing node[%i] = %s" % (node, nodes[node]))
				path = self.host_path_lookup(nodes[node])
				self.store[path][5] = "Connecting..."
				self.statusbar.push(self.online, ("Forming a swarm with %i nodes..." % interval))
				
				host_t = threading.Thread(target=self.ssh_connect, args=(nodes[node], path, ssh_nodes,))

				host_t.start()
				#host_threads.append(host_t)

#			with outlock:
				# Connecting monitors
			#print (ssh_nodes)
			
			while len(ssh_nodes) != interval:
				#print ("Waiting.. (%i != %i)" % (len(ssh_nodes), len(nodes)))
				
				text = ("Waiting properly establishment of nodes' swarm (%i of %i)..." % (len(ssh_nodes), interval))
				self.set_statusbar(text)
				Gtk.main_iteration()
				
			for monitor in range (0, len(monitors)):

				#print ("SSHing monitor[%i] = %s" % (monitor, monitors[monitor]))
				path = self.host_path_lookup(monitors[monitor])
				self.store[path][5] = "Connecting..."
					
				host_t = threading.Thread(target=self.ssh_connect, args=(nodes[node], path, ssh_monitors,))

				host_t.start()
				
			while len(ssh_monitors) != len(monitors):
				self.set_statusbar("Connecting monitors (%i of %i)..." % (len(ssh_monitors), len(monitors)))
				Gtk.main_iteration()
					
			self.set_statusbar("Virtual Network formmed!")
			#if self.store[path][5] != "Connected":
			#	print ("Error sending command to %s" % self.store[path][1])
			#else:
			#	self.set_statusbar("Running command...")
					
		return ssh_nodes, ssh_monitors

	
	def ssh_connect (self, host, path, queue):
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		
		try:
			ssh.connect(host, username='rnp_OSN', key_filename=self.connection.private_key, timeout=10.0)
			self.store[path][5] = "Connected"
			queue.append(ssh)
			return ssh
			
		except:
			self.store[path][5] = "Could not connect"
			return None
			
	
	def get_nodes (self, node_type=None):
		i = len(self.store)
		connected = []
		disconnected = []
		
		if node_type == "monitor":
			node_column = 3
		else:
			node_column = 2
		
		for num in range(0, i):
			node = self.store[num]

			if node[node_column] == True:
				if node[4] == Gtk.STOCK_CONNECT:
					connected.append(node[1])
				else:
					disconnected.append(node[1])
		
		nodes = (connected, disconnected)
		return nodes
	
	def selAllclicked (self, widget):
		i = len(self.store)
		
		for num in range(0, i):
			#print (len(self.store[num]))
			node = self.store[num]
			
			if node[3] != True:
				node[2] = 1
				self.total_nodes = self.total_nodes + 1
				
				self.set_statusbar("%d nodes and %d monitors selected" % (self.total_nodes, self.total_monitors))
	
	def addCheck_node (self, nodes):
		host_icon_status = Gtk.STOCK_DIALOG_QUESTION
		host_threads = []
		i = len(nodes)
		
		for num in range(0, i):

			#host_t = threading.Thread(target=GObject.idle_add, args=(self.check_availability, planetlab_connection, num,))
			host_t = threading.Thread(target=self.check_availability, args=(nodes, num,))

			host_t.start()
			host_threads.append(host_t)

		#for host_t in host_threads:
		
		#	while host_t.is_alive():
		#		host_t.join()

	def on_save_menu_file(self, treeViewSelection):
		f = open(self.nodes_file, 'w')
		i = len(self.store)
		
		for num in range(0, i):
			#print (len(self.store[num]))
			node = self.store[num]
			line = str(node[0]) + ' ' + node[1] + ' ' + str(node[2]) + ' ' + str(node[3]) + '\n'
			f.write (line)
		
		
	def set_icon(self, nodes, num, node_icon_status):		
		self.store.append([nodes[num]['node_id'], nodes[num]['hostname'], False, False, node_icon_status])

		#tree = Gtk.TreeView(store)
		#column = Gtk.TreeViewColumn("ID and Host")

		#host_id = Gtk.CellRendererText()
		#hostname = Gtk.CellRendererText()

		#column.pack_start(host_id, True)
		#column.pack_start(hostname, True)

		#column.add_attribute(host_id, "text", 0)
		#column.add_attribute(hostname, "text", 1)

		#tree.append_column(column)
		#treeview.app	end(tree)

	def check_availability(self, nodes, num):
		
		#user_name = connection.getUsername()
		#user_name = "rnp_OSN"
		print ("[%i] - %s" % (num, nodes[num]))
		
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		host = nodes[num]['hostname'].rstrip()
		try:
		#with outlock:
			ssh.connect(host, username='rnp_OSN', key_filename=self.connection.private_key, timeout=10.0)
			print("Connecting to [%i] %s..." % (num, nodes[num]['hostname']))
			ssh.close()
			#with outlock:
			#self.set_icon(nodes, num, Gtk.STOCK_CONNECT)
			self.store.append([nodes[num]['node_id'], nodes[num]['hostname'], False, False, Gtk.STOCK_CONNECT, "Disconnected"])
			with outlock:
				self.online = self.online + 1

			#self.store.append([self.nodes[num]['node_id'], self.nodes[num]['hostname'], False, False, Gtk.STOCK_CONNECT])
			#outlock.release()
		#self.store.append([nodes[num]['node_id'], nodes[num]['hostname'], False, False, Gtk.STOCK_CONNECT])
				#stdin, stdout, stderr = ssh.exec_command("uptime")
				#type(stdin)
				#print (stdout.readlines())
				
		except:
		#	print ("Unexpected error:", sys.exc_info()[0])
			print ("Error connecting to %s.." % nodes[num]['hostname'])
			with outlock:	
				self.store.append([nodes[num]['node_id'], nodes[num]['hostname'], False, False, Gtk.STOCK_MEDIA_RECORD, "Disconnected"])
				self.offline = self.offline + 1
				#print ("SSH: There was an error")

		self.statusbar.push(self.online, ("There are %i online nodes and %i offline nodes" % (self.online, self.offline)))

	def show_message_dlg(self, text, msg_type=None, msg_title=None):
		"""This Function is used to show an error dialog when
		an error occurs.
		error_string - The error string that will be displayed
		on the dialog.
		"""
		
		button = Gtk.ButtonsType.OK
		
		if msg_type == Gtk.MessageType.ERROR:
			first_msg = "Error"
			button = Gtk.ButtonsType.CLOSE
			
		elif msg_type == Gtk.MessageType.INFO:
			first_msg = "Information"
			# button is already set
			
		elif msg_type == Gtk.MessageType.QUESTION:
			first_msg = "Question"
			button = Gtk.ButtonsType.YES_NO
		
		if msg_title:
			title = msg_title
			
		if msg_type == None:
			msg_type = Gtk.MessageType.INFO
			button = Gtk.ButtonsType.NONE
		
		widget = Gtk.Window.__init__(self.builder.get_object("message"), title=msg_title)
		#widget.set_modal(False)
		#box = Gtk.Box(spacing=6)
		#window.add(box)
		
		self.msgDialog = Gtk.MessageDialog(widget, Gtk.DialogFlags.DESTROY_WITH_PARENT, msg_type, button, msg_title)
		#self.msgDialog.set_modal(True)
		self.msgDialog.format_secondary_text(text)
		answer = self.msgDialog.run()
		self.msgDialog.destroy()
		#self.msgDialog = None
		
		return answer
		
	def on_cell_status_toggled(self, widget, path):
		self.store[path][3] = not self.store[path][3]

		if self.store[path][2]:
			self.store[path][2] = False
			self.total_nodes = self.total_nodes - 1
			
		if self.store[path][3]:
			self.total_monitors = self.total_monitors + 1
		else:
			self.total_monitors = self.total_monitors - 1
			
		self.set_statusbar("%d nodes and %d monitors selected" % (self.total_nodes, self.total_monitors))
		#selection = self.treeview.get_selection()
		#selection.unselect_path(self.treeview.get_path_at_pos(0, 0))

		#print path
		for item in self.store:
			if item[3]:
				print (item[3])
				
	def on_cell_toggled(self, widget, path):
		self.store[path][2] = not self.store[path][2]
		
		if self.store[path][3]:
			self.store[path][3] = False
			self.total_monitors = self.total_monitors - 1
			
		if self.store[path][2]:
			self.total_nodes = self.total_nodes + 1
		else:
			self.total_nodes = self.total_nodes - 1

		self.set_statusbar("%d nodes and %d monitors selected" % (self.total_nodes, self.total_monitors))
			
		for item in self.store:
			if item[2]:
				print (item[1])
			
	def on_dirview_toggled (self, widget, path, node):

		i = len(self.workDirContent)
		
		if self.workDirContent[path][0] == Gtk.STOCK_DIRECTORY:
			self.show_message_dlg("You cannot select a folder to be executed.", Gtk.MessageType.ERROR, "Folder Selected")
			
		else:
			for unset in range(0, i):
				if unset == int(path):
					self.workDirContent[path][node] = not self.workDirContent[path][node]
					if self.workDirContent[path][node]:
						filename = os.path.basename(self.workDirContent[path][1])
						dirname = os.path.basename(self.workDirPath)
						fullpath = '/home/' + self.connection.getSliceName() + '/' + dirname + '/'
						cmd = 'bridge.sh'
						
						if node == 2:
							self.node_remoteCmd = fullpath + cmd + ' ' + fullpath + ' ' + filename
							self.node_kill = filename
							print (self.node_remoteCmd)
						else:
							self.monitor_remoteCmd = fullpath + cmd + ' ' + fullpath + ' ' + filename
							self.monitor_kill = filename
							print (self.monitor_remoteCmd)
						
					else:
						if node == 2:
							self.node_remoteCmd = None
						else:
							self.monitor_remoteCmd = None
				else:
					self.workDirContent[unset][node] = False

	def set_statusbar(self, text):
		self.statusbar.push(0, text)
			
	def dirview(self):
		treeview = self.builder.get_object("dirview")
	
		self.workDirContent = Gtk.ListStore(str, str, bool, bool, str)
		treeview.set_model(self.workDirContent)

		icon_column = Gtk.TreeViewColumn('', Gtk.CellRendererPixbuf(), stock_id=0)
		treeview.append_column(icon_column)
		
		name_column = Gtk.TreeViewColumn("Name", Gtk.CellRendererText(), text=1)
		name_column.set_resizable(True)
		name_column.set_sort_column_id(1)
		treeview.append_column(name_column)
		
		node_toggle = Gtk.CellRendererToggle()
		#node_toggle.connect("toggled", self.on_cell_toggled)
		#node_toggle.connect("toggled", self.on_dirview_node_toggled)
		node_toggle.connect("toggled", self.on_dirview_toggled, 2)
		column_toggle = Gtk.TreeViewColumn("Execute in Node", node_toggle, active=2)
		treeview.append_column(column_toggle)
		
		monitor_toggle = Gtk.CellRendererToggle()
		monitor_toggle.connect("toggled", self.on_dirview_toggled, 3)
		monitor_column_toggle = Gtk.TreeViewColumn("Execute in Monitor", monitor_toggle, active=3)
		monitor_column_toggle.set_resizable(True)
		treeview.append_column(monitor_column_toggle)
		
		size_column = Gtk.TreeViewColumn("Size (KB)", Gtk.CellRendererText(), text=4)
		size_column.set_resizable(True)
		size_column.set_sort_column_id(4)
		treeview.append_column(size_column)
