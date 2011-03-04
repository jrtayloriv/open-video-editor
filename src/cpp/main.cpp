#include <fltk/Window.h>
#include <fltk/Widget.h>
#include <fltk/file_chooser.h>
#include <fltk/run.h>
#include <fltk/MenuBuild.h>

static void open_cb () {
  //In File menu have an "Open..." option
    //If File->Open is clicked, then we do this
    fltk::file_chooser("Pick a file", NULL, NULL, NULL);
}

static void exit_cb () {
  //In File menu have an "Open..." option
    //If File->Open is clicked, then we do this
    return;
}

  //create a menu bar with a File menu and a Playback menu
static void build_menus(fltk::MenuBar * menu, fltk::Widget *w) {
    fltk::ItemGroup * g;
    menu->user_data(w);
    menu->begin();
      g = new fltk::ItemGroup( "&File" );
      g->begin();
        new fltk::Item( "&Open File...",    fltk::COMMAND + 'o', (fltk::Callback *)open_cb );
        new fltk::Divider();
        new fltk::Item( "E&xit", fltk::COMMAND + 'q', (fltk::Callback *)exit_cb, 0 );
      g->end();
    menu->end();
}

using namespace fltk;

int main(int argc, char **argv) {
  Window *window = new Window(640, 480);
  window->begin();
  Widget *box = new Widget(20, 40, 640, 480, "Main window - file dialog and video port");
  box->box(UP_BOX);
  box->labelfont(HELVETICA_BOLD);
  box->labelsize(16);
  box->labeltype(SHADOW_LABEL);

  MenuBar *menu = new MenuBar(0,0,640,20, NULL);
  build_menus(menu,window);

  window->end();
  window->show(argc, argv);

  return run();
}



