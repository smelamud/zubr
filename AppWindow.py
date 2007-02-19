# @(#) $Id$
# -*- coding: utf8 -*-

import pygtk
pygtk.require('2.0')
import gtk

from StartScreen import StartScreen
from ExamScreen import ExamScreen
from PauseScreen import PauseScreen
from FinishScreen import FinishScreen
from Examiner import Examiner

class AppWindow(gtk.Window):

    def __init__(self, filename = None):
	gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
	self.running = False

	self.setExamTitle('')
	self.set_position(gtk.WIN_POS_CENTER)
	self.set_border_width(10)
	self.set_resizable(True)
	screen = self.get_screen()
	self.resize(600, 300)
	self.connect('destroy', self.destroy)

	self.examiner = Examiner()

	self.screens = {
	    'start': StartScreen(self),
	    'exam': ExamScreen(self),
	    'pause': PauseScreen(self),
	    'finish': FinishScreen(self),
	}
	if filename != None:
	    self.screens['start'].file.set_filename(filename)
	self.currentScreen = None

    def setExamTitle(self, title):
	if not title:
	    self.set_title(u'Зубр')
	else:
	    self.set_title(u'Зубр - ' + title)

    def switchScreen(self, name):
	if self.currentScreen:
	    self.currentScreen.hide()
	self.currentScreen = self.screens[name]
	self.currentScreen.show()

    def run(self):
	self.running = True
	self.switchScreen('start')
	self.show()
	gtk.main()

    def destroy(self, widget, data = None):
	gtk.Window.destroy(self)
	if self.running:
	    gtk.main_quit()
