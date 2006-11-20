# @(#) $Id$
# -*- coding: utf8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import pango

from Screen import Screen

class StartScreen(Screen):

    def __init__(self, window):
	Screen.__init__(self, window, gtk.VBox(False))

	label = gtk.Label(u'Начнем-с...')
	label.modify_font(pango.FontDescription('bold'))
	self.container.pack_start(label, True, False)

	bbox = gtk.HButtonBox()
	bbox.set_spacing(5)
	bbox.set_layout(gtk.BUTTONBOX_END)
	self.container.pack_start(bbox, False)

	button = gtk.Button(stock = gtk.STOCK_GO_FORWARD)
	button.connect('clicked', self.start)
	bbox.pack_start(button)

	button = gtk.Button(stock = gtk.STOCK_CLOSE)
	button.connect('clicked', self.window.destroy)
	bbox.pack_start(button)

    def start(self, widget, data = None):
	self.window.switchScreen('exam')
