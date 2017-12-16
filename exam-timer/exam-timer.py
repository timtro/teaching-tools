#!/usr/bin/env python3

import argparse
from enum import Enum
import datetime as dt
from time import strftime

from gi.repository import Gtk, Gdk, GObject


class State(Enum):
    PAUSED = 0
    RUNNING = 1


class ClockWindow:

    def __init__(self, duration):

        self.timeRemains = duration
        self.timeOfLastCall = dt.datetime.now()

        self.state = State.PAUSED

        self.win = Gtk.Window()
        self.win.connect("delete-event", Gtk.main_quit)
        self.win.set_title("Clock")

        # Create the vertical container
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.win.add(vbox)

        self.timetext = Gtk.Label()
        self.timetext.set_justify(Gtk.Justification.CENTER)
        self.remainstext = Gtk.Label()
        self.remainstext.set_justify(Gtk.Justification.CENTER)
        self.progressbar = Gtk.ProgressBar()
        self.progressbar.set_inverted(True)
        vbox.pack_start(self.timetext, True, True, 0)
        vbox.pack_start(self.remainstext, True, True, 0)
        vbox.pack_start(self.progressbar, True, True, 25)
        # self.win.add(self.timetext)
        self.win.set_border_width(25)
        self.win.maximize()
        self.win.connect('key_press_event', on_key_press_event)
        self.win.show_all()
        self.BW = False
        return None

    def update(self):
        if self.state is State.RUNNING:
            now = dt.datetime.now()
            self.timeRemains -= now - self.timeOfLastCall
            self.timeOfLastCall = now

        self.timetext.set_markup(
            "Current Time:\n<span size='98000'>" + strftime('%H:%M') + "</span>")
        self.remainstext.set_markup("Time Remaining:\n<span size='98000'>" + '{0:02d}'.format(
            self.timeRemains.seconds // 3600) + ':' + '{0:02d}'.format((self.timeRemains.seconds // 60) % 60) + "</span>")
        self.progressbar.set_fraction(
            self.timeRemains.seconds / duration.seconds)

        # As this is a timeout function, return True so that it
        # continues to get called
        return True

    def toggle_pause(self):
        if self.state == State.PAUSED:
            self.state = State.RUNNING
            self.timeOfLastCall = dt.datetime.now()
        else:
            self.state = State.PAUSED

    def toggle_black_and_white(self):
        if self.BW == True:
            self.BW = False
            self.timetext.modify_fg(Gtk.StateFlags.NORMAL, None)
            self.remainstext.modify_fg(Gtk.StateFlags.NORMAL, None)
            self.win.override_background_color(Gtk.StateFlags.NORMAL, None)
        else:
            self.timetext.modify_fg(
                Gtk.StateFlags.NORMAL, Gdk.color_parse("white"))
            self.remainstext.modify_fg(
                Gtk.StateFlags.NORMAL, Gdk.color_parse("white"))
            self.win.override_background_color(
                Gtk.StateFlags.NORMAL, Gdk.RGBA(0.0, 0.0, 0.0, 1.0))
            self.BW = True


class EntryWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Entry Demo")
        self.set_size_request(200, 100)

        self.timeout_id = None

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.entry = Gtk.Entry()
        self.entry.set_text("Hello World")
        vbox.pack_start(self.entry, True, True, 0)

        hbox = Gtk.Box(spacing=6)
        vbox.pack_start(hbox, True, True, 0)

        self.check_editable = Gtk.CheckButton("Editable")
        self.check_editable.connect("toggled", self.on_editable_toggled)
        self.check_editable.set_active(True)
        hbox.pack_start(self.check_editable, True, True, 0)

        self.check_visible = Gtk.CheckButton("Visible")
        self.check_visible.connect("toggled", self.on_visible_toggled)
        self.check_visible.set_active(True)
        hbox.pack_start(self.check_visible, True, True, 0)

        self.pulse = Gtk.CheckButton("Pulse")
        self.pulse.connect("toggled", self.on_pulse_toggled)
        self.pulse.set_active(False)
        hbox.pack_start(self.pulse, True, True, 0)

        self.icon = Gtk.CheckButton("Icon")
        self.icon.connect("toggled", self.on_icon_toggled)
        self.icon.set_active(False)
        hbox.pack_start(self.icon, True, True, 0)

    def on_editable_toggled(self, button):
        value = button.get_active()
        self.entry.set_editable(value)

    def on_visible_toggled(self, button):
        value = button.get_active()
        self.entry.set_visibility(value)

    def on_pulse_toggled(self, button):
        if button.get_active():
            self.entry.set_progress_pulse_step(0.2)
            # Call self.do_pulse every 100 ms
            self.timeout_id = GObject.timeout_add(100, self.do_pulse, None)
        else:
            # Don't call self.do_pulse anymore
            GObject.source_remove(self.timeout_id)
            self.timeout_id = None
            self.entry.set_progress_pulse_step(0)

    def do_pulse(self, user_data):
        self.entry.progress_pulse()
        return True

    def on_icon_toggled(self, button):
        if button.get_active():
            stock_id = Gtk.STOCK_FIND
        else:
            stock_id = None
        self.entry.set_icon_from_stock(Gtk.EntryIconPosition.PRIMARY,
                                       stock_id)


def on_key_press_event(widget, event):
    keyname = Gdk.keyval_name(event.keyval)
    print("Key %s (%d) was pressed" % (keyname, event.keyval))
    if keyname == 'c':
        ClockWindow.toggle_black_and_white(clockWin)
    if keyname == 'p':
        ClockWindow.toggle_pause(clockWin)
    if keyname == 'o':
        owin = EntryWindow()
        owin.show_all()


def undoBWColor(X):
    X.label.modify_fg(Gtk.StateFlags.NORMAL, None)
    X.win.override_background_color(Gtk.StateFlags.NORMAL, None)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='A simple timer to be projected on screen during an academic examination.')
    parser.add_argument('-m', '--mins', type=int,
                        help='Exam duration in minutes.')
    args = parser.parse_args()

    # now = dt.datetime.now()
    duration = dt.timedelta(minutes=args.mins)

    settings = Gtk.Settings.get_default()
    settings.set_property("gtk-application-prefer-dark-theme", True)

    clockWin = ClockWindow(duration)

    # add to the main loop scheduled tasks
    GObject.timeout_add(200, clockWin.update)
    Gtk.main()
