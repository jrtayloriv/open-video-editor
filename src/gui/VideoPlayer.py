#!/usr/bin/env python

import sys, os, time, thread
import glib, gtk, gobject
import pygst
pygst.require("0.10")
import gst

class VideoPlayer:
    'Video playback widget'
    #   * TODO: create class VideoPortal embedded in Window with 
    #           VideoControlToolbar ... VideoPortal should be
    
    
    def __init__(self):
        self.window = gtk.Window()
        self.window.connect('destroy', self.on_destroy)

        self.drawingarea = gtk.DrawingArea()
        self.drawingarea.connect('realize', self.on_drawingarea_realized)
        self.window.add(self.drawingarea)

        self.playbin = gst.element_factory_make('playbin2')

        self.sink = gst.element_factory_make('xvimagesink')
        self.sink.set_property('force-aspect-ratio', True)
        self.playbin.set_property('video-sink', self.sink)

        self.bus = self.playbin.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message::eos", self.on_finish)

    def play(self, video_stream):
        self.playbin.set_property('uri', 'file://' + video_stream)
        self.window.show_all()
        self.playbin.set_state(gst.STATE_PLAYING)

    def on_finish(self, bus, message):
        self.playbin.set_state(gst.STATE_PAUSED)

    def on_destroy(self, window):
        self.playbin.set_state(gst.STATE_NULL)
        self.window.destroy()

    def on_drawingarea_realized(self, sender):
        self.sink.set_xwindow_id(self.drawingarea.window.xid)


