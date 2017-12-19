#!/usr/bin/env python3

import argparse
from enum import Enum
import datetime as dt
from time import strftime

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject

normalColur = "#FFFFFF"
pausedColour = "#BBBBBB"
endedColour = "#FF9090"


class State(Enum):
    PAUSED = 0
    RUNNING = 1


class ClockWindow:
    def __init__(self, duration):

        self.timeRemains = duration
        self.originalDuration = duration
        self.timeOfLastCall = dt.datetime.now()
        self.countDownColour = "#FFFFFF"
        self.pause()

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
        if self.timeRemains <= dt.timedelta(seconds=1):
            self.countDownColour = endedColour
        else:
            if self.state is State.RUNNING:
                now = dt.datetime.now()
                self.timeRemains -= now - self.timeOfLastCall
                self.timeOfLastCall = now

        self.timetext.set_markup("Current Time:\n<span size='98000'>" +
                                 strftime('%H:%M') + "</span>")

        if self.timeRemains <= dt.timedelta(seconds=60):
            self.remainstext.set_markup(
                "Time Remaining:\n<span size='98000' color='" +
                self.countDownColour + "'>" + '{0:02d}'.format(
                    self.timeRemains.seconds) + " s</span>")
            self.progressbar.set_fraction(self.timeRemains.seconds /
                                          self.originalDuration.seconds)
        else:
            self.remainstext.set_markup(
                "Time Remaining:\n<span size='98000' color='" +
                self.countDownColour + "'>" + '{0:02d}'.format(
                    self.timeRemains.seconds // 3600) + ':' + '{0:02d}'.format(
                        (self.timeRemains.seconds // 60) % 60) + "</span>")
            self.progressbar.set_fraction(self.timeRemains.seconds /
                                          self.originalDuration.seconds)

        # Return True so that it continues to get called
        return True

    def toggle_pause(self):
        if self.state == State.PAUSED:
            self.unpause()
        else:
            self.pause()

    def unpause(self):
        self.state = State.RUNNING
        self.countDownColour = normalColur
        self.timeOfLastCall = dt.datetime.now()

    def pause(self):
        self.state = State.PAUSED
        self.countDownColour = pausedColour

    def toggle_black_and_white(self):
        if self.BW == True:
            self.BW = False
            self.timetext.modify_fg(Gtk.StateFlags.NORMAL, None)
            self.remainstext.modify_fg(Gtk.StateFlags.NORMAL, None)
            self.win.override_background_color(Gtk.StateFlags.NORMAL, None)
        else:
            self.timetext.modify_fg(Gtk.StateFlags.NORMAL,
                                    Gdk.color_parse("white"))
            self.remainstext.modify_fg(Gtk.StateFlags.NORMAL,
                                       Gdk.color_parse("white"))
            self.win.override_background_color(Gtk.StateFlags.NORMAL,
                                               Gdk.RGBA(0.0, 0.0, 0.0, 1.0))
            self.BW = True

    def add_time(self, delta):
        self.timeRemains += delta
        if self.originalDuration < self.timeRemains:
            self.originalDuration = self.timeRemains

    def deduct_time(self, delta):
        if self.timeRemains > delta:
            self.timeRemains -= delta


def on_key_press_event(widget, event):
    keyname = Gdk.keyval_name(event.keyval)
    # print("Key %s (%d) was pressed" % (keyname, event.keyval))
    if keyname == 'c':
        ClockWindow.toggle_black_and_white(clockWin)
    elif event.keyval == Gdk.KEY_space:
        ClockWindow.toggle_pause(clockWin)
    elif event.keyval == Gdk.KEY_Left and (event.state &
                                           Gdk.ModifierType.CONTROL_MASK):
        ClockWindow.add_time(clockWin, dt.timedelta(seconds=1))
    elif event.keyval == Gdk.KEY_Right and (event.state &
                                            Gdk.ModifierType.CONTROL_MASK):
        ClockWindow.deduct_time(clockWin, dt.timedelta(seconds=1))
    elif event.keyval == Gdk.KEY_Up and (event.state &
                                         Gdk.ModifierType.CONTROL_MASK):
        ClockWindow.add_time(clockWin, dt.timedelta(minutes=1))
    elif event.keyval == Gdk.KEY_Down and (event.state &
                                           Gdk.ModifierType.CONTROL_MASK):
        ClockWindow.deduct_time(clockWin, dt.timedelta(minutes=1))


def undoBWColor(X):
    X.label.modify_fg(Gtk.StateFlags.NORMAL, None)
    X.win.override_background_color(Gtk.StateFlags.NORMAL, None)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='A simple timer to be projected on screen during an academic examination.'
    )
    parser.add_argument(
        '-m', '--mins', type=int, help='Exam duration in minutes.')
    args = parser.parse_args()

    # now = dt.datetime.now()
    durationFromArgs = dt.timedelta(minutes=args.mins)

    settings = Gtk.Settings.get_default()
    settings.set_property("gtk-application-prefer-dark-theme", True)

    clockWin = ClockWindow(durationFromArgs)

    # add to the main loop scheduled tasks
    GObject.timeout_add(200, clockWin.update)
    Gtk.main()
