# @(#) $Id$
# -*- coding: utf8 -*-

import pygtk
pygtk.require('2.0')
import gtk

from Screen import Screen

class StartScreen(Screen):

    def __init__(self, window):
	Screen.__init__(self, window, gtk.HBox(False))

	vbox = gtk.VBox(False)
	self.container.pack_start(vbox, True, False)
	button = gtk.Button(stock = gtk.STOCK_GO_FORWARD)
	button.connect('clicked', self.start)
	vbox.pack_start(button, True, False)

    def start(self, widget, data = None):
	self.window.switchScreen('exam')
