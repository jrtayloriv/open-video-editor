###############################################################
# WidgetLibrary.py - a library of commonly used GUI components
#
#  * This is where we store customized widgets as well as commonly used 
#    core widgets like gtk.FileSelectionDialog (which we'll actually probably
#    subclass into a customized version)
###############################################################

# The reason this goes here instead of in MainWindow, is that this is a generic dialog
# that will be needed by many GUI components besides just MainWindow
# On the other hand MainWindow.MainMenuBar is a uniquely MainWindow widget, so we include it there...
class FileSelectDialog(gtk.FileSelection):
    # Right now all this does is print the file name to the console.
    # What we should do is have this open the file and play it.
    # If OK is clicked, then print selected filename to console
    def file_ok_sel(self, w):
        print "I would have opened %s for playback if I was a real video editor." % self.get_filename()

    def destroy(self, widget):
   return 0;

    def __init__(self):
        # Create a new file selection widget
        self.set_title("Select a file: ")

        self.connect("destroy", self.destroy)

        # Connect the ok_button to file_ok_sel method
        self.ok_button.connect("clicked", self.file_ok_sel)
    
        # Connect the cancel_button to destroy the widget
        self.cancel_button.connect("clicked", lambda w: self.destroy())