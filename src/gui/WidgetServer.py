###########################################################################
# WidgetServer.py -- Wrapper around pyGTK functions/widgets for OVE modules
###########################################################################

* Decouples OVE GUI from GTK
  * Right now is just a GTK wrapper
  * Can later extend to serve up widgets from multiple GUI libraries.
  
* Manages our most commonly used custom widgets (timelines, 
  video panels, etc.) and configurations for widgets

* If plugin authors want GUI capabilities for their plugins, this is
  the module they talk to. They just add callbacks to the WidgetServer
  and add Widget descriptions in the WidgetLibrary (this lets us cache 
  commonly used widgets, etc.)
  
  
  Questions:
    Q: What would be the relation of this to MainWindow
    A: I think what we'd do is have it where MainWindow is requested 
       just like any other custom Widget in the WidgetLibrary ... 