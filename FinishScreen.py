# @(#) $Id: StartScreen.py 22 2007-02-06 22:36:37Z balu $
# -*- coding: utf8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import pango

from Screen import Screen
from ExamScreen import Scoreboard

class FinishScreen(Screen):

    def __init__(self, window):
	Screen.__init__(self, window, gtk.VBox(False))

	label = gtk.Label(u'Тренировка закончена.')
	label.modify_font(pango.FontDescription('bold 12'))
	self.container.pack_start(label, True, False)

	self.scoreboard = Scoreboard(window.examiner)
	self.container.pack_start(self.scoreboard, True, False)

	bbox = gtk.HButtonBox()
	bbox.set_spacing(5)
	bbox.set_layout(gtk.BUTTONBOX_END)
	self.container.pack_start(bbox, False)

	button = gtk.Button(stock = gtk.STOCK_MEDIA_REWIND)
	button.connect('clicked', self.rewind)
	bbox.pack_start(button)

	button = gtk.Button(stock = gtk.STOCK_CLOSE)
	button.connect('clicked', self.window.destroy)
	bbox.pack_start(button)

    def show(self):
	Screen.show(self)
	self.scoreboard.refresh()

    def rewind(self, widget = None):
	self.window.switchScreen('start')
