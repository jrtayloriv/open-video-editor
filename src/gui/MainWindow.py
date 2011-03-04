#!/usr/bin/env python

###########################################################
# mainwindow.py: Main editor window w/ tabbed panels for:
#    * Filesystem tree
#    * Clip Editor
#    * Project manager / clip bin
#    * Python terminal
#
# Later on, we will generate interface from GUI template files 
###########################################################

import pygtk
pygtk.require('2.0')
import gtk
import pygst
pygst.require('0.10')

class MainWindow():
    #Event handler for "open_file_dialog" signal	

    def __init__(self):

	    # Set window properties
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Open Video Editor 0.01a")
        self.window.set_size_request(500, 350)
        self.window.set_border_width(10)
        self.window.connect("destroy", lambda w: gtk.main_quit())

        #create a container that can hold multiple widgets, and place the menu
        #bar into this container, then add the container to self.window ... the
        #reason we have to do this is that gtk.Window is a "gtk.Bin" which can
        #only contain a single child widget (including dialogs) ...
 
        #Create a gtk.MenuBar and pack it into the window for display
        menu_bar = self.main_menu_bar()
        vbox = gtk.VBox(False, 2)
        vbox.pack_start(menu_bar, False, False, 0)
        vbox.show()
        self.window.add(vbox)
        
        # Add the following in a gtk.Notebook (below menubar)
        # * File browser
        # * Clips / Sequences
        #   * When we open a file from the file selector, it adds them here
        #   * Once a file is on the list here, we can right-click "Play file"
        # * Clip editor

        self.window.show_all()

    # We should do this with Glade 
    def main_menu_bar(self):
        'Top menu bar widget for main window'
        menu_bar = gtk.MenuBar()

        #"File" menu
        file_menu_item = gtk.MenuItem("File")
        file_menu = gtk.Menu()
        file_menu_item.set_submenu(file_menu)

        open_menu_item = gtk.MenuItem("Open file...")
        open_menu_item.connect("activate", self.open_file)
        file_menu.append(open_menu_item)

        exit_menu_item = gtk.MenuItem("Exit")
        exit_menu_item.connect("activate", gtk.main_quit)
        file_menu.append(exit_menu_item)

        menu_bar.append(file_menu_item)

        #"Help" menu
        help_menu_item = gtk.MenuItem("Help")
        help_menu = gtk.Menu()
        help_menu_item.set_submenu(help_menu)

        online_help_menu_item = gtk.MenuItem("Online help ...")
        online_help_menu_item.connect("activate", self.launch_online_help)
        help_menu.append(online_help_menu_item)

        about_menu_item = gtk.MenuItem("About")
        about_menu_item.connect("activate", self.about_dialog)
        help_menu.append(about_menu_item)

        menu_bar.append(help_menu_item)

        menu_bar.show()
        return menu_bar

    def open_file(self, widget):
        'display file selection dialog, and return filehandle for file selected'
        open_file_dialog = gtk.FileChooserDialog("Open..",
            None,
            gtk.FILE_CHOOSER_ACTION_OPEN,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
            gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        #open_file_dialog.show()
        #self.window.add(file_dialog)
        open_file_dialog.run()

        #This is where we'd normally determine what to do with the filename
        #the user selected ... right now it just directly calls video_play.
        #...but later it will hand the filehandle back to someone who will
        #determine what to do with it ...
        file_selected = open_file_dialog.get_filename()

        print "DEBUG: About to open: %s" % file_selected
        self.video_play(file_selected)

        #Clean up
        open_file_dialog.destroy()

    def video_play(self, video_stream):
        'play video_stream using video playback library (either gstreamer playbin or ffplay)'

        #XXX: For now, we're just playing with ffplay
        #import os
        #ffplay_status = os.system("ffplay '%s'" % video_stream)
        #print "DEBUG: ffplay exited with status code %d" % ffplay_status

        #TODO: Create VideoPlayer class that uses gstreamer
        import VideoPlayer        
        video_player = VideoPlayer.VideoPlayer()       #vid windows will look to config for which player to use
        video_player.play(video_stream)

    # Should also be local help eventually (generated from online help docs)
    def launch_online_help(self, widget):
        'launch the default browser, and send them to wiki'
        pass

    #Later this would come out of a config file (which would also feed ove --version, etc.)
    def about_dialog(self, widget):
        'Show "About" dialog when Help->About is selected'
        about = gtk.AboutDialog()
        about.set_program_name("Open Video Editor")
        about.set_version("0.01a")
        about.set_copyright("(c) Jesse R. Taylor (jrtayloriv@gmail.com)")
        about.set_comments("An open-source video editing suite, written in Python.")
        about.set_website("http://github.com/jrtayloriv/open-video-editor")
        about.run()
        about.destroy()
    

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    MainWindow()
    main()


