#!/usr/bin/env python

import sys, os, time, thread
import glib, gtk, gobject
import pygst
pygst.require("0.10")
import gst

class VideoPlayer:
    'Video playback widget:  video portal + control/timeline widgets'
    #   * TODO: break out playbin/sink stuff into VideoPortal class
    #           embedded in Container with a VideoControlToolbar, with
    #           VideoPlayer as the object containing the window that they
    #           live in, and acting as interface for them.
    
    # Essentially, the VideoPortal will have an input stream (perhaps from 
    # a Clip or Sequence object), filters, and
    # then output to some sort of sink ... note that everything other than
    # the sink part is handled by non-gui components (in io/)
    
    # The VideoControlToolbar will send commands to the backend for the 
    # portal's video stream (whichever portal the Toolbar is connected to,
    # that is)
    
    # The VideoPlayer will act as a container for each of these, and will 
    # handle communications with other GUI components
    
    def __init__(self):
        # XXX: Later, this needs to be a gtk.Frame that gets placed inside 
        #      a Panel
        self.window = gtk.Window()
        self.window.connect('destroy', self.on_destroy)
        # How do we place this on the right margin of screen, and make it the
        # same width as MainWindow?
        
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


