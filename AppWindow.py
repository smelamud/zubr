# @(#) $Id$
# -*- coding: utf8 -*-

import pygtk
pygtk.require('2.0')
import gtk

from StartScreen import StartScreen
from ExamScreen import ExamScreen

class AppWindow(gtk.Window):

    currentScreen = None

    def __init__(self):
	gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)

	self.set_position(gtk.WIN_POS_CENTER)
	self.set_title(u'Зубрёжка')
	self.set_border_width(10)
	self.set_resizable(True)
	self.connect('destroy', self.destroy)

	self.screens = {
	    'start': StartScreen(self),
	    'exam': ExamScreen(self),
	}

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
