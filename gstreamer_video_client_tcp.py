import sys, os
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, Gtk

from gi.repository import GdkX11, GstVideo

class GTK_Main(object):
	def __init__(self):
		window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
		window.set_title("Client")
		window.set_default_size(500, 400)
		window.connect("destroy", Gtk.main_quit, "WM destroy")
		window.show_all()
	
		pipeline = Gst.Pipeline.new("client")
		src = Gst.ElementFactory.make("filesrc", "source")
		src.set_property("location", "C:/Users/admin/Documents/course/socket_programming/project/gstreamer/python27_test/test1.mp4")
		pipeline.add(src)
		
		client = Gst.ElementFactory.make("tcpclientsink", "client")
		pipeline.add(client)
		client.set_property("host", "127.0.0.1")
		client.set_property("port", 3000)
		src.link(client)

		pipeline.set_state(Gst.State.PLAYING)
		
		
		
GObject.threads_init()
Gst.init(None)
GTK_Main()
Gtk.main()