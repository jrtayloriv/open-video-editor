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
import pygst   # XXX: Of course, we shouldn't be importing GST here ... 
               #      but it's just for testing the GUI with video
pygst.require('0.10')
import gst

class MainWindow():
    #Event handler for "open_file_dialog" signal	

    def __init__(self):

	    # Set window properties
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Open Video Editor 0.01a")
        self.window.set_size_request(750, 450)
        self.window.set_border_width(10)
        self.window.connect("destroy", lambda w: gtk.main_quit())

        #create a container that can hold multiple widgets, and place the menu
        #bar into this container, then add the container to self.window ... the
        #reason we have to do this is that gtk.Window is a "gtk.Bin" which can
        #only contain a single child widget (including dialogs) ...
 
        #Create a gtk.MenuBar and pack it into the window for display
        menu_bar = self.main_menu_bar()

        ########################################
        # Add the following in a gtk.Notebook: (below menubar)
        # * File browser
        # * Clips / Sequences
        #   * When we open a file from the file selector, it adds them here
        #   * Once a file is on the list here, we can right-click "Play file"
        # * Clip editor
        #################################3
        tabbed_panels = MainWindowTabbedPanels()        

        vbox = gtk.VBox(False, 2)
        vbox.pack_start(menu_bar, False, False, 0)
        vbox.pack_start(tabbed_panels.table, False, False, 0)
        vbox.show()
        self.window.add(vbox)
 
        #All aboard ... show the window, and all of it's child widgets
        self.window.show_all()

    def main_menu_bar(self):
        'Top menu bar widget for main window'
        menu_bar = gtk.MenuBar()

        #"File" menu
        file_menu_item = gtk.MenuItem("File")
        file_menu = gtk.Menu()
        file_menu_item.set_submenu(file_menu)

        open_menu_item = gtk.MenuItem("Open file...")
        open_menu_item.connect("activate", self.open_file_clicked)
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

    # What this should do is create a new Clip object, and add the File to
    # the list of Files in clip_obj.files ... 
    def open_file_clicked(self, widget):
        'Callback for when user clicks "Open File" in the "File" menu'
        file_selected = self.open_file_dialog()
        # XXX: Check to make sure the file path got returned        
        #print "DEBUG: About to play: %s" % file_selected
        self.video_play(file_selected)

    def open_file_dialog(self):
        'Display file selection dialog, and return full path to file selected'
        
        dialog = gtk.FileChooserDialog("Open..",
            None,
            gtk.FILE_CHOOSER_ACTION_OPEN,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
            gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        #open_file_dialog.show()
        #self.window.add(file_dialog)
        dialog.run()

        #Store full path to file selected by user
        file_selected = dialog.get_filename()

        #Clean up
        dialog.destroy()

        return file_selected

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


######################################################################
# This is where we keep the tabbed control panels for the main window
# with a different row of buttons at the bottom of each tabbed panel.
######################################################################
class MainWindowTabbedPanels:
    def __init__(self):
        
        # XXX: We shouldn't be calling GTK+ functions directly like this, in case we need to change interface libs later.
        #      Instead, we should have a wrapper around gtk.Notebook() called GUILibsWrapper.TabbedContainer()
        
        # XXX: Nor should we have the notebook, buttons, and table all in one megaclass ...

        # XXX: Nor are these always going to be part of the MainWindow panel -- we are going to have dockable dialogs like Gimp
        #      i.e., they should be able to "break off" tabs into separate windows if they want two or more open at once.

        #Create a table to hold Notebook and Buttons
        #JT: It might be a good thing that we're managing the tables here, so that when we add
        #    tab break-off functionality, the tab manager can update both the table and notebook
        self.table = gtk.Table(3,6,gtk.FALSE)
        
        # Create a new notebook, place the position of the tabs
        self.notebook = gtk.Notebook()
        self.notebook.set_tab_pos(gtk.POS_TOP)
        
        self.table.attach(self.notebook, 0,6,0,1)
        self.notebook.show()
        self.show_tabs = gtk.TRUE
        self.show_border = gtk.TRUE
        
        # XXX: This is where we would create our own labels for the tabs
        # Let's append a bunch of pages to the notebook
        for i in range(3):
            bufferf = "Append Frame %d" % (i+1)
            bufferl = "Page %d" % (i+1)

            frame = gtk.Frame(bufferf)
            frame.set_border_width(10)
            frame.set_usize(350, 350)
            frame.show()

            label = gtk.Label(bufferf)
            frame.add(label)
            label.show()

            label = gtk.Label(bufferl)
            self.notebook.append_page(frame, label)
      
        # Now let's add a page to a specific spot
        checkbutton = gtk.CheckButton("Check me please!")
        checkbutton.set_usize(100, 75)
        checkbutton.show ()

        label = gtk.Label("Add page")
        self.notebook.insert_page(checkbutton, label, 2)

        # Now finally let's prepend pages to the notebook
        for i in range(3):
            bufferf = "Prepend Frame %d" % (i+1)
            bufferl = "PPage %d" % (i+1)

            frame = gtk.Frame(bufferf)
            frame.set_border_width(10)
            frame.set_usize(100, 75)
            frame.show()

            label = gtk.Label(bufferf)
            frame.add(label)
            label.show()

            label = gtk.Label(bufferl)
            self.notebook.prepend_page(frame, label)
    
        # Set what page to start at (page 4)
        self.notebook.set_page(3)

        #These should be per-tab ... 
        #So each gtk.Notebook page needs to have a button toolbar attached ...

        # Create a bunch of buttons
        button = gtk.Button("close")
        button.connect("clicked", self.delete)
        self.table.attach(button, 0,1,1,2)
        button.show()

        button = gtk.Button("next page")
        button.connect("clicked", self.notebook.next_page)
        self.table.attach(button, 1,2,1,2)
        button.show()

        button = gtk.Button("prev page")
        button.connect("clicked", self.notebook.prev_page)
        self.table.attach(button, 2,3,1,2)
        button.show()

        button = gtk.Button("tab position")
        button.connect("clicked", self.rotate_book, self.notebook)
        self.table.attach(button, 3,4,1,2)
        button.show()

        button = gtk.Button("tabs/border on/off")
        button.connect("clicked", self.tabsborder_book, self.notebook)
        self.table.attach(button, 4,5,1,2)
        button.show()

        button = gtk.Button("remove page")
        button.connect("clicked", self.remove_book, self.notebook)
        self.table.attach(button, 5,6,1,2)
        button.show()

        self.table.show()

               
    # This method rotates the position of the tabs    
    def rotate_book(self, button):
        self.notebook.set_tab_pos((self.notebook.get_tab_pos()+1) %4)

    # Add/Remove the page tabs and the borders
    def tabsborder_book(self, button):
        tval = gtk.FALSE
        bval = gtk.FALSE
        if self.show_tabs == gtk.FALSE:
            tval = gtk.TRUE 
        if self.show_border == gtk.FALSE:
            bval = gtk.TRUE
            
        self.notebook.set_show_tabs(tval)
        self.show_tabs = tval
        self.notebook.set_show_border(bval)
        self.show_border = bval

    # Remove a page from the notebook
    def remove_book(self, button):
        page = self.notebook.get_current_page()
        self.notebook.remove_page(page)
        # Need to refresh the widget -- 
        # This forces the widget to redraw itself.
        self.notebook.draw((0,0,-1,-1))

    def delete(self, widget, event=None):
        self.destroy()
        

            
def main():
    # From the GTK+ docs: 
    #   "The GTK+ main loop's primary role is to listen for
    #   events on a file descriptor connected to the X server, and forward 
    #   them to widgets."
    gtk.main()
    return 0

if __name__ == "__main__":
    MainWindow()
    main()


