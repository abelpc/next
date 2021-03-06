import os
from gi.repository import Gtk
from listNodes import *
from inconnect import *
from dialog import *

class Handler:
	
	def __init__(self, bldr):
		self.builder = bldr
		self.connection = Connect()

	def onDeleteWindow(self, *args):
        	Gtk.main_quit(*args)
        	
	def closeWindow(self, widget):
        	window = widget.get_window()
        	window.destroy()

	def on_button_press_event(self, treeview, event):
		print ("EVENT")
		popup = self.builder.get_object("menu4")
		treeview.get_tree_view().grab_focus()
		if event.button == 3:
			print ("RIght-click")
			popupItem = self.builder.get_object("menuitem5")

			x = int(event.x)
			y = int(event.y)
			time = event.time

			#treeViewSelection = treeview.get_selection()
			treeViewSelection = treeview
			(model, pathList) = treeViewSelection.get_selected_rows()
			
			#treeViewSelection.select_path(pathList)
			print ("Model: %s" % model)
			print ("PathList: %s" % pathList)
			treeIter = model.get_iter(pathList)
			value = model.get_value(treeIter, 1)
			print ("VALOR: %s" % value)

			#treeview = treeview.get_tree_view()
			#pthinfo = treeview.get_path_at_pos(x, y)
			#if pthinfo is not None:
			#	print ("Inside")
			#	path, col, cellx, celly = pthinfo

			popupItem.set_label(value)
			#	treeIter = model.get_iter(path)
			treeview.get_tree_view().grab_focus()
			#	treeview.set_cursor( model, pathList, 0)
			popup.popup( None, None, None, None, event.button, time)
			return True

	def onButtonPressed(self, widget):
		dialog = Dialog(self.builder, None)
		user = self.builder.get_object("username").get_text()
		password = self.builder.get_object("password").get_text()
		#user = "abelpc_uff@yahoo.com.br"
		#password = "dkwpq753"
		#print "User: %s\nPassword: %s" % (user, password)
		
		if (not user or not password):
			dialog.show_message_dlg("Please, provide BOTH Username and Password.", Gtk.MessageType.INFO)
			
		else:
			if 1 == 1:
#			if self.connection.check_connectivity():
			
				planetlab_connection = listNodes()
			
				if planetlab_connection.authenticate(user, password):
				
					#planetlab_connection.check_availability(planetlab_connection)
					
					self.closeWindow(widget)
					directory = os.path.abspath('..')
					final_dir = os.path.join(directory, user)
					if (not os.path.isdir(final_dir)):
						try:
							os.makedirs(final_dir)
						except:
							dialog.show_message_dlg(("It was not possible to write in the %s directory. You will not be able to save your work." % directory), Gtk.MessageType.ERROR)
						
					self.main_dialog = Dialog(self.builder, "mainDialog", planetlab_connection)

					#window2 = builder.get_object("mainWindow")
					#window2.show()
				else:
					dialog.show_message_dlg("Invalid Username and/or Password", Gtk.MessageType.INFO)
			else:
				dialog.show_message_dlg("Network Connection Unavailable")


	def on_tAdd_clicked(self, widget):
		self.add_dialog = Dialog(self.builder, "addDlg")
			
	def on_menu_clicked(self, treeViewSelection):
	
		(model, pathList) = treeViewSelection.get_selected_rows()
		
		for path in pathList:
			treeIter = model.get_iter(path)
			value = model.get_value(treeIter, 0)
			print ("Black listing %s..." % value)
			model.remove(treeIter)
			#print self.main_dialog.store[item[0]].get_indices()
			#for index in item:
			#	print self.main_dialog.store[item][index]
		
	def on_tDel_clicked(self, treeViewSelection):
		#print "Del Button"
		
		(model, pathList) = treeViewSelection.get_selected_rows()
		
		for path in pathList:
			treeIter = model.get_iter(path)
			value = model.get_value(treeIter, 0)
			#print "Removendo %s..." % value
			model.remove(treeIter)
			#print self.main_dialog.store[item[0]].get_indices()
			#for index in item:
			#	print self.main_dialog.store[item][index]


	def on_first_main_destroy(self, object, data=None):
		#print "quit with cancel"
		Gtk.main_quit()
		
