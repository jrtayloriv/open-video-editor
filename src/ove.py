#Open Video Editor - 0.01a

#All we're going to do here for now is get a window going with a file browser that can open videos in a video portal (separate window)

import gobject
gobject.threads_init()
import gst
import pygtk
pygtk.require("2.0")
import gtk
gtk.gdk.threads_init()
import sys
import os

###############
# Main window
##############



###############
# Video portal
###############

# Use the gstreamer or ffmpeg viewers, rather than rolling your own :)
