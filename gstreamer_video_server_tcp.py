'''
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst, Gtk

GObject.threads_init()
Gst.init()
 
# Callback for the decodebin source pad
#def new_decode_pad(dbin, pad, islast):
def new_decode_pad(dbin, pad):
        #pad.link(convert.get_pad("sink")) => no get_pad
		pad.link(convert.get_static_pad("sink")) # 用 sink 勉強可以
		#pad.link(convert.get_static_pad("video_sink")) => None
		
 
# create a pipeline and add [tcpserversrc ! decodebin ! audioconvert ! alsasink]
pipeline = Gst.Pipeline.new("server")
 
tcpsrc = Gst.ElementFactory.make("tcpserversrc", "source")
pipeline.add(tcpsrc)
tcpsrc.set_property("host", "127.0.0.1")
tcpsrc.set_property("port", 3000)
 
decode = Gst.ElementFactory.make("decodebin", "decode")
#decode.connect("new-decoded-pad", new_decode_pad)
decode.connect("pad-added", new_decode_pad)
pipeline.add(decode)
tcpsrc.link(decode)

#convert = Gst.ElementFactory.make("videoconvert", "video-convert")
convert = Gst.ElementFactory.make("audioconvert", "convert")
pipeline.add(convert)

#sink = Gst.ElementFactory.make("d3dvideosink", "video-output")
sink = Gst.ElementFactory.make("directsoundsink", "sink")
pipeline.add(sink)
convert.link(sink)
 
pipeline.set_state(Gst.State.PLAYING)
 
# enter into a mainloop
loop = GObject.MainLoop()
loop.run()
'''

import sys, os
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, Gtk

from gi.repository import GdkX11, GstVideo

def new_decode_pad(dbin, pad):
	pad.link(GTK_Main.convert.get_static_pad("sink")) # 用 sink 勉強可以
	#pad.link(convert.get_static_pad("video_sink")) => None

class GTK_Main(object):
	convert = ''

	def __init__(self):
		window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
		window.set_title("Server")
		window.set_default_size(500, 400)
		window.connect("destroy", Gtk.main_quit, "WM destroy")
		window.show_all()
	
		# create a pipeline and add [tcpserversrc ! decodebin ! audioconvert ! alsasink]
		pipeline = Gst.Pipeline.new("server")
		 
		tcpsrc = Gst.ElementFactory.make("tcpserversrc", "source")
		pipeline.add(tcpsrc)
		tcpsrc.set_property("host", "127.0.0.1")
		tcpsrc.set_property("port", 3000)
		 
		decode = Gst.ElementFactory.make("decodebin", "decode")
		#decode.connect("new-decoded-pad", new_decode_pad)
		decode.connect("pad-added", new_decode_pad)
		pipeline.add(decode)
		tcpsrc.link(decode)

		#GTK_Main.convert = Gst.ElementFactory.make("videoconvert", "video-convert")
		GTK_Main.convert = Gst.ElementFactory.make("audioconvert", "convert")
		pipeline.add(GTK_Main.convert)

		#sink = Gst.ElementFactory.make("d3dvideosink", "video-output")
		sink = Gst.ElementFactory.make("directsoundsink", "sink")
		pipeline.add(sink)
		GTK_Main.convert.link(sink)
		 
		pipeline.set_state(Gst.State.PLAYING)



GObject.threads_init()
Gst.init(None)
GTK_Main()
Gtk.main()