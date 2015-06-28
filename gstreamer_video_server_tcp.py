#!/usr/bin/env python
#-*-coding:utf-8-*-

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

	#pad.link(GTK_Main.convert.get_static_pad("sink")) # 用 sink 勉強可以
	#pad.link(convert.get_static_pad("video_sink")) => None

class GTK_Main(object):
	audio_convert = ''
	video_convert = ''

	def __init__(self, IP, recv_port):
		window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
		window.set_title("Server")
		window.set_default_size(500, 400)
		window.connect("destroy", Gtk.main_quit, "WM destroy")
		window.show_all()
	
		# create a pipeline and add [tcpserversrc ! decodebin ! audioconvert ! alsasink]
		pipeline = Gst.Pipeline.new("server")
		 
		tcpsrc = Gst.ElementFactory.make("tcpserversrc", "source")
		pipeline.add(tcpsrc)
		tcpsrc.set_property("host", IP)
		tcpsrc.set_property("port", recv_port)
		 
		decode = Gst.ElementFactory.make("decodebin", "decode")
		decode.connect("pad-added", new_decode_pad)
		pipeline.add(decode)
		tcpsrc.link(decode)

		GTK_Main.video_convert = Gst.ElementFactory.make("videoconvert", "video-convert")
		GTK_Main.audio_convert = Gst.ElementFactory.make("audioconvert", "convert")
		pipeline.add(GTK_Main.video_convert)
		pipeline.add(GTK_Main.audio_convert)

		video_sink = Gst.ElementFactory.make("d3dvideosink", "video-output")
		audio_sink = Gst.ElementFactory.make("directsoundsink", "sink")
		pipeline.add(video_sink)
		pipeline.add(audio_sink)
		GTK_Main.video_convert.link(video_sink)
		GTK_Main.audio_convert.link(audio_sink)
		 
		pipeline.set_state(Gst.State.PLAYING)

if __name__ == '__main__':
	parser = argparse.ArgumentParser( description = "IP RECV_PORT" )
	parser.add_argument("ip", help="specify relay server IP")
	parser.add_argument("recv_port", help="specify recving port", type=int)
	args = parser.parse_args()

	GObject.threads_init()
	Gst.init(None)
	GTK_Main(args.ip, args.recv_port)
	Gtk.main()
