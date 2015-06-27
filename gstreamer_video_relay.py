import sys, os
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, Gtk

from gi.repository import GdkX11, GstVideo

def new_decode_pad(dbin, pad):
	if pad.get_name() == "src_0":
		#video
		pad.link(GTK_Main.video_convert.get_static_pad("sink"))
	else:
		#audio
		pad.link(GTK_Main.audio_convert.get_static_pad("sink"))

	#pad.link(GTK_Main.convert.get_static_pad("sink")) # 用 sink 勉強可以
	#pad.link(convert.get_static_pad("video_sink")) => None

class GTK_Main(object):
	audio_convert = ''
	video_convert = ''

	def __init__(self):
		window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
		window.set_title("Server")
		window.set_default_size(500, 400)
		window.connect("destroy", Gtk.main_quit, "WM destroy")
		window.show_all()
	
		# create a pipeline and add [tcpserversrc ! decodebin ! audioconvert ! alsasink]
		pipeline = Gst.Pipeline.new("relay server")
		 
		tcpsrc = Gst.ElementFactory.make("tcpserversrc", "source")
		pipeline.add(tcpsrc)
		tcpsrc.set_property("host", "127.0.0.1")
		tcpsrc.set_property("port", 3000)
		 
		tcpsink = Gst.ElementFactory.make("tcpclientsink", "sink")
		pipeline.add(tcpsink)
		tcpsink.set_property("host", "127.0.0.1")
		tcpsink.set_property("port", 3001)
		tcpsrc.link(tcpsink)

		 
		pipeline.set_state(Gst.State.PLAYING)


GObject.threads_init()
Gst.init(None)
GTK_Main()
Gtk.main()