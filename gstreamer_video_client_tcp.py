#!/usr/bin/env python
#-*-coding:utf-8-*-
import sys, os
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, Gtk
from gi.repository import GdkX11, GstVideo

import argparse

class GTK_Main(object):
	def __init__(self, IP, send_port):
		window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
		window.set_title("Client")
		window.set_default_size(500, 400)
		window.connect("destroy", Gtk.main_quit, "WM destroy")
		window.show_all()
	
		pipeline = Gst.Pipeline.new("client")
		src = Gst.ElementFactory.make("filesrc", "source")
		src.set_property("location", "C:/Users/CNA/Desktop/GStreamer/test1.mp4")
		pipeline.add(src)
		
		client = Gst.ElementFactory.make("tcpclientsink", "client")
		pipeline.add(client)
		client.set_property("host", IP)
		client.set_property("port", send_port)
		src.link(client)

		pipeline.set_state(Gst.State.PLAYING)
		
if __name__ == '__main__':	
	parser = argparse.ArgumentParser( description = "IP SEND_PORT" )
	parser.add_argument("ip", help="specify relay server IP")
	parser.add_argument("send_port", help="specify sending port", type=int)
	args = parser.parse_args()

	GObject.threads_init()
	Gst.init(None)
	GTK_Main(args.ip, args.send_port)
	Gtk.main()
