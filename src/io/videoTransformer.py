#####################
# VideoTransformer.py
#####################

* We want an object that applies a filter or transform to a video/audio stream passing through it. Gstreamer and ffmpeg already offer this

* Gstreamer is at a higher-level of abstraction than ffmpeg. ffmpeg is a raw-data transformer. Gstreamer is a multi-media stream library (think C stream vs. raw io functions ...) 

* This is the interface between gst-python and the OVE modules

* This will enable us to use alternative video stream processing facilities later

* Blender works with python as its internal scripting language ... it would be extremely useful to use Blender's timeline facilities and 3D object modelling tools here ...