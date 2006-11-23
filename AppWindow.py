# @(#) $Id$
# -*- coding: utf8 -*-

import pygtk
pygtk.require('2.0')
import gtk

from StartScreen import StartScreen
from ExamScreen import ExamScreen
from Examiner import Examiner

class AppWindow(gtk.Window):

    examiner = None
    currentScreen = None

    def __init__(self):
	gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)

	self.set_position(gtk.WIN_POS_CENTER)
	self.set_title(u'Зубрёжка')
	self.set_border_width(10)
	self.set_resizable(True)
	screen = self.get_screen()
	self.resize(screen.get_width() / 2, screen.get_height() / 2)
	self.connect('destroy', self.destroy)

	self.screens = {
	    'start': StartScreen(self),
	    'exam': ExamScreen(self),
	}

	self.examiner = Examiner()

    def switchScreen(self, name):
	if self.currentScreen:
	    self.currentScreen.hide()
	self.currentScreen = self.screens[name]
	self.currentScreen.show()

    def run(self):
	self.switchScreen('start')
	self.show()
	gtk.main()

    def destroy(self, widget, data = None):
	gtk.main_quit()