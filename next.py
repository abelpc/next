from gi.repository import Gtk, GObject
from listNodes import *
from inconnect import *
from handler import *
from dialog import *

GObject.threads_init()
builder = Gtk.Builder()
builder.add_from_file("anv2.glade")
builder.connect_signals(Handler(builder))
connection = Connect()

window = builder.get_object("first_main")
window.show_all()

Gtk.main()
