import os
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, Gtk


class GTK_Main:
	audio_convert = ""

	def __init__(self):
		window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
		window.set_title("Webcam-Viewer")
		window.set_default_size(500, 400)
		window.connect("destroy", Gtk.main_quit, "WM destroy")
		
		vbox = Gtk.VBox()
		window.add(vbox)
		self.movie_window = Gtk.DrawingArea()
		vbox.add(self.movie_window)
		hbox = Gtk.HBox()
		vbox.pack_start(hbox, False, False, 0)
		hbox.set_border_width(10)
		hbox.pack_start(Gtk.Label(), False, False, 0)
		self.button = Gtk.Button("Start")
		self.button.connect("clicked", self.start_stop)
		hbox.pack_start(self.button, False, False, 0)
		self.button2 = Gtk.Button("Quit")
		self.button2.connect("clicked", self.exit)
		hbox.pack_start(self.button2, False, False, 0)
		hbox.add(Gtk.Label())
		window.show_all()
		
		# video
		self.player = Gst.Pipeline.new("server - video")
		src = Gst.ElementFactory.make("udpsrc")
		src.set_property("port", 3000)
		self.player.add(src)
		
		
		capsfilter = Gst.ElementFactory.make("capsfilter")
		capsfilter.set_property("caps", Gst.Caps.from_string("video/x-theora,width=640,height=480"))
		self.player.add(capsfilter)
		src.link(capsfilter)
		
		videodec = Gst.ElementFactory.make("theoradec")
		self.player.add(videodec)
		capsfilter.link(videodec)
		
		converter = Gst.ElementFactory.make("videoconvert")
		self.player.add(converter)
		videodec.link(converter)
		
		videosink = Gst.ElementFactory.make("d3dvideosink")
		self.player.add(videosink)
		converter.link(videosink)


		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self.on_message)
		bus.connect("sync-message::element", self.on_sync_message)
		
		# audio
		self.player2 = Gst.Pipeline.new("server - audio")
		audiosrc = Gst.ElementFactory.make("udpsrc")
		audiosrc.set_property("port", 3001)
		self.player2.add(audiosrc)

		audio_capsfilter = Gst.ElementFactory.make("capsfilter")
		audio_capsfilter.set_property("caps", Gst.Caps.from_string("audio/x-raw,format=(endianness=1234,signed=true,width=16,depth=16,rate=22000,channels=1)"))
		self.player2.add(audio_capsfilter)
		audiosrc.link(audio_capsfilter)
		
		audio_decoder = Gst.ElementFactory.make("vorbisdec", "audio_decoder")
		self.player2.add(audio_decoder)
		audio_capsfilter.link(audio_decoder)
		
		audio_converter = Gst.ElementFactory.make("audioconvert", "audio_convert")
		self.player2.add(audio_converter)
		audio_decoder.link(audio_converter)
		
		audiosink = Gst.ElementFactory.make("directsoundsink", "soudsink")
		self.player2.add(audiosink)
		audio_converter.link(audiosink)
		
	def start_stop(self, w):
		if self.button.get_label() == "Start":
			self.button.set_label("Stop")
			self.player.set_state(Gst.State.PLAYING)
			self.player2.set_state(Gst.State.PLAYING)
		else:
			self.player.set_state(Gst.State.NULL)
			self.player2.set_state(Gst.State.NULL)
			self.button.set_label("Start")
			
	def exit(self, widget, date=None):
		Gtk.main_quit()
		
	def on_message(self, bus, message):
		t = message.type
		if t == Gst.MessageType.EOS:
			self.player.set_state(Gst.State.NULL)
			self.player2.set_state(Gst.State.NULL)
			self.button.set_label("Start")
		elif t == Gst.MessageType.ERROR:
			err, debug = message.parse_error()
			print("Error: %s"%err, debug.encode('utf-8'))
			self.player.set_state(Gst.State.NULL)
			self.player2.set_state(Gst.State.NULL)
			self.button.set_label("Start")
			
	def on_sync_message(self, bus, message):
		struct = message.get_structure()
		if not struct:
			return
		message_name = struct.get_name()
		print(message_name)
		if message_name == 'preapre-xwindow-id':
			print('preapre-xwindow-id')
			imagesink = message.src
			imagesink.set_property('force-aspect-ratio', True)
			imagesink.set_xwindow_id(self.movie_window.window.xid)
			
Gst.init(None)
GTK_Main()
GObject.threads_init()
Gtk.main()