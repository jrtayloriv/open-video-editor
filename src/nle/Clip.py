# Clips are video segments + timeline + metadata

# I don't really see why we would want to differentiate between a clip and a "sequence"
# ... they are both just layered sets of video segments. It seems like that would be more
# of a UI difference, rather than a difference in representation .. 

# Most editors have a Timeline that is where the main video project is being built from a bunch of video segments.
# This main timeline is what gets rendered. But what we're going to do is design our Clip structure to be the equivalent
# of one of these (i.e. something that we can stack and sequentially arrange multiple video/audio segments and then render
# them into a single video output stream). This makes it where we have a single data type that works for all clips, any one
# of which can be rendered ... We are getting rid of the concept of the single timeline per project ... This allows us to 
# open multiple files into a clip structure (clip_a), edit these clips in the timeline editor to make a complex multi-source video,
# ... then we can treat this clip as if it were a video segment, placing it inside another Clip (clip_b), but still be able to come back later and rearrange the individual segments that comprise clip_a (think gimp -- we haven't merged layers yet...) ... every Clip should be playable in a VideoPlayer, every Clip should be Render/Export-able, and every clip should be able to have multiple tracks of video/audio segments.

# The final result of combining all the segments into a single video/audio stream is a ClipPipeline

# A ClipPipeline is a wrapper around Pipeline, which is your generic media stream pipeline building library
# At first Pipeline will be a thin wrapper around gstreamer's pipeline/bin interface

import Timeline
import os.path

#Clip:
# * Sequence of (VideoSegment, start_location) pairs
# * 

class Clip:
    'A Clip is just a set of video segments (pieces of files marked by in/out pts) placed on a Timeline'
    
    #XXX: Shouldn't we be passing in a segment, instead of the video file
    #    (since we need in/out anyway)?
    
    # Clips don't need to know about files. They only contain segments
    # ... the FileToClipImporter would be called by ClipLibrary or perhaps 
    # ClipEditor ... it would be the only module that knows about both Clips
    # and Files and can facilitate things where we need that like importing 
    # a video stream into a clip
    
    #If we pass the initializer a VideoSegment, it will create a new Clip with
    #that VideoSegment's start point at zero sec.
    def __init__(self, video_segment=Null):

        # Create timeline structure for Clip ... we place video segments at
        # points on the timeline (segments can overlap though -- i.e. layers,
        # for transparency effects later ...)
        self.timeline = Timeline()
                
        #List of files that comprise the clip, their in/out points, and location on clip timeline
        if os.path.exists(video_file):
            #open video file and convert to clip
            self.file_to_segment(self, video_file)
            
            
    def load_video_file(self, video_file):
        #test if file exists
        #if it does, import it and gather metadata about it, which we store in ClipInfo object ...
        if os.path.exists(video_file):
            #file_handle = get file handle ...
            #self.files.append(file_handle)
            pass
    
    # XXX: We don't go directly from stream to clip. 
    #      We go from data --> stream --> segment --> clip.segments.append(segment)
    #      So instead of a stream_to_clip function, we'll have
    #      .add_segment(), which will add a segment that is
    #      handed to us from god knows where ... since we don't
    #      have to do playback, we don't have to know anything about
    #      segments or even what a segment is. All we have to knows is that it
    #      has a file, an in point, and an out point and that we use clips to
    #      place them at a certain point on the timeline (by either specifying
    #      where to place the in point, or specifying where to place the out
    #      point
    def place_segment_inpoint(self, stream, ):
        'Takes a stream (generally a local file, and converts it to a clip)'
        pass

#XXX: Is this object overkill? Why can't we just do this in a Clip method for now?
#JT: I don't think so, because it makes the Clip interface simpler (since this way
#    Clip only deals with VideoSegments, instead of both Files && VideoSegments
class FileToClipImporter:
    'Open a file, convert it to a segment, and place it on a Clip\'s timeline'

    def __init__(self):
        pass
    
    

# See "Chapter 12. Metadata" of gstreamer manual for information about 
# video stream metadata tagging in gstreamer ... but this shouldn't be
# at the clip level ...
class ClipInfo:
    'Holds metadata about the clip (total playing time, etc.)'
    def __init__(self):
        pass

# Can segments live anywhere other than clips? If so, they shouldn't be here ...
class Segment: 