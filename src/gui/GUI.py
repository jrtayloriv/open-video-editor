* This is just a wrapper around the different GUI libs (GTK+, Qt, fltk, etc.)

* This is the lowest-level API that plugin developers target for their plugins' GUI widgets

* Creates MainWindow ... etc.

* Windows and panels ... "Windows" contain a Notebook that we can snap our Panels in and out of. 
When we snap a Panel in, its gtk.Frame gets embeded in a Notebook page. When we snap one of these
tabs out, the gtk.Frame gets embedded in a gtk.Window ...

* Need method of saving configuration/layout of GUI.