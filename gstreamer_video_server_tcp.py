import sys, os
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, Gtk
from gi.repository import GdkX11, GstVideo

import argparse

def new_decode_pad(dbin, pad):
	if pad.get_name() == "src_0":
		#video
		pad.link(GTK_Main.video_convert.get_static_pad("sink"))
	else:
		#audio
		pad.link(GTK_Main.audio_convert.get_static_pad("sink"))

class GTK_Main(object):
	audio_convert = ''
	video_convert = ''

	def __init__(self):
		window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
		window.set_title("Server")
		window.set_default_size(500, 400)
		window.connect("destroy", Gtk.main_quit, "WM destroy")
		
		vbox = Gtk.VBox()
		window.add(vbox)
		
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
		
		window.show_all()
	
		# create a pipeline and add [tcpserversrc ! decodebin ! audioconvert ! alsasink]
		self.pipeline = Gst.Pipeline.new("server")
		 
		self.tcpsrc = Gst.ElementFactory.make("tcpserversrc", "source")
		self.pipeline.add(self.tcpsrc)
		
		 
		decode = Gst.ElementFactory.make("decodebin", "decode")
		decode.connect("pad-added", new_decode_pad)
		self.pipeline.add(decode)
		self.tcpsrc.link(decode)

		GTK_Main.video_convert = Gst.ElementFactory.make("videoconvert", "video-convert")
		GTK_Main.audio_convert = Gst.ElementFactory.make("audioconvert", "convert")
		self.pipeline.add(GTK_Main.video_convert)
		self.pipeline.add(GTK_Main.audio_convert)

		video_sink = Gst.ElementFactory.make("d3dvideosink", "video-output")
		audio_sink = Gst.ElementFactory.make("directsoundsink", "sink")
		self.pipeline.add(video_sink)
		self.pipeline.add(audio_sink)
		GTK_Main.video_convert.link(video_sink)
		GTK_Main.audio_convert.link(audio_sink)

		
	def start_stop(self, w):
		if self.button.get_label() == "Start":
			# set IP, Port
			self.tcpsrc.set_property("host", self.IPEntry.get_text().strip())
			self.tcpsrc.set_property("port", int(self.portEntry.get_text().strip(), base=10))
				
			# start playing
			self.pipeline.set_state(Gst.State.PLAYING)
			
			self.button.set_label("Stop")
		else:
			# stop receiving video stream
			self.pipeline.set_state(Gst.State.NULL)
				
			self.button.set_label("Start")


if __name__ == '__main__':
	GObject.threads_init()
	Gst.init(None)
	GTK_Main()
	Gtk.main()