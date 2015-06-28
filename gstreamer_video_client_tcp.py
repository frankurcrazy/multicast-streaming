#!/usr/bin/env python
#-*-coding:utf-8-*-
import sys, os
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, Gtk
from gi.repository import GdkX11, GstVideo

import argparse

class GTK_Main(object):
	def __init__(self):
		window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
		window.set_title("Client")
		window.set_default_size(500, 400)
		window.connect("destroy", Gtk.main_quit, "WM destroy")
		window.show_all()
	
		vbox = Gtk.VBox()
		window.add(vbox)
		
		
		# entry for filename
		hboxVideo = Gtk.HBox()
		vbox.pack_start(hboxVideo, False, False, 0)
		self.videoEntry= Gtk.Entry()
		videoTextView = Gtk.TextView()
		videoTextView.get_buffer().set_text("Video Name : ")
		videoTextView.set_editable(False)
		videoTextView.set_cursor_visible(False)
		hboxVideo.add(videoTextView)
		hboxVideo.add(self.videoEntry)
		
		# entry for IP
		hboxIP = Gtk.HBox()
		vbox.pack_start(hboxIP, False, False, 0)
		self.IPEntry = Gtk.Entry()
		IPTextView = Gtk.TextView()
		IPTextView.get_buffer().set_text("IP : ")
		IPTextView.set_editable(False)
		IPTextView.set_cursor_visible(False)
		hboxIP.add(IPTextView)
		hboxIP.add(self.IPEntry)
		
		# entry for port
		hboxPort = Gtk.HBox()
		vbox.pack_start(hboxPort, False, False, 0)
		portTextView = Gtk.TextView()
		portTextView.get_buffer().set_text("Port : ")
		portTextView.set_editable(False)
		portTextView.set_cursor_visible(False)
		self.portEntry = Gtk.Entry()
		hboxPort.add(portTextView)
		hboxPort.add(self.portEntry)
		
		# start/stop button
		hboxButton = Gtk.HBox()
		vbox.pack_start(hboxButton, False, False, 0)
		self.button = Gtk.Button("Start")
		hboxButton.pack_start(self.button, False, False, 0)
		self.button.connect("clicked", self.start_stop)
		
		# create textview for displaying error message
		self.textview = Gtk.TextView()
		vbox.pack_start(self.textview, False, False, 0)
		
		window.show_all()
		
		# send out the video stream
		self.pipeline = Gst.Pipeline.new("client")
		self.src = Gst.ElementFactory.make("filesrc", "source")
		
		self.pipeline.add(self.src)
		
		self.client = Gst.ElementFactory.make("tcpclientsink", "client")
		self.pipeline.add(self.client)
		self.src.link(self.client)

		# play on the local
		self.player = Gst.ElementFactory.make("playbin", "player")
		
	def start_stop(self, w):
		if self.button.get_label() == "Start":
			filepath = self.videoEntry.get_text().strip()

			if os.path.isfile(filepath):
				#clear error message
				self.textview.get_buffer().set_text("File is not exist")
			
				filepath = os.path.realpath(filepath)
				self.button.set_label("Stop")
				
				# set filepath
				self.player.set_property("uri", "file:///"+filepath)
				self.src.set_property("location", filepath)
				
				# set IP, Port
				self.client.set_property("host", self.IPEntry.get_text().strip())
				self.client.set_property("port", int(self.portEntry.get_text().strip(), base=10))
				
				# start playing
				self.player.set_state(Gst.State.PLAYING)
				self.pipeline.set_state(Gst.State.PLAYING)
			else:
				# display error message
				self.textview.get_buffer().set_text("File is not exist")
				
				# stop playing on the local
				self.player.set_state(Gst.State.NULL)
				
				# stop sending video stream
				self.pipeline.set_state(Gst.State.NULL)
				
				self.button.set_label("Start")	
		else:
			# stop playing on the local
			self.player.set_state(Gst.State.NULL)
			
			# stop sending video stream
			self.pipeline.set_state(Gst.State.NULL)
			
			self.button.set_label("Start")
		
	
if __name__ == '__main__':	
	GObject.threads_init()
	Gst.init(None)
	GTK_Main()
	Gtk.main()