# XXX: I think Gstreamer already has this ... see gst.Clock
#      Let's just write a wrapper around gst.Clock (with more sensible names)

#Actually, see "Chapter 11. Position tracking and seeking" from the gstreamer manual:
# "Media players, for example, will want to show a slider showing the progress in the song, and usually also a label indicating stream length. #Transcoding applications will want to show a progress bar on how much percent of the task is done. GStreamer has built-in support for doing all #this using a concept known as querying."

import pygst
pygst.require("0.10")
import gst

class Timeline:
    ' ... but it\'s a timeline for our tracks
     ... it starts at 0 and goes to +inf ... has a cursor you can seek with which
     starts at 0 by default'
    def __init__(self, cursor_position=0):
        
        #create timeline that goes from 0 --> inf+ ... 
        
        #initialize cursor
        set_cursor_position(cursor_position)

    def set_cursor_position(self, cursor_position):
        self.cursor_position = cursor_position
        