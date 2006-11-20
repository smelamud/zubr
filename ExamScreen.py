# @(#) $Id$
# -*- coding: utf8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import pango

from Screen import Screen

class ExamScreen(Screen):

    def __init__(self, window):
	Screen.__init__(self, window, gtk.VBox(False, 20))

	label = gtk.Label()
	label.set_markup(u'<span foreground="#00CC00">0</span>/' \
	    u'<span foreground="#FF0000">2</span>/3 23 сек')
	label.set_alignment(0.5, 0)
	self.container.pack_start(label, False)

	label = gtk.Label(u'Вопрос')
	label.set_alignment(0, 1)
	self.container.pack_start(label)

	label = gtk.Label(u'Верно')
	label.set_alignment(0, 0)
	label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color(0, 32767, 0))
	label.modify_font(pango.FontDescription('bold'))
	self.container.pack_start(label, False)

	hbox = gtk.HBox(False, 5)
	self.container.pack_start(hbox, False)

	entry = gtk.Entry()
	hbox.pack_start(entry)

	button = gtk.Button(stock = gtk.STOCK_OK)
	hbox.pack_start(button, False)

	bbox = gtk.HButtonBox()
	bbox.set_layout(gtk.BUTTONBOX_END)
	self.container.pack_start(bbox, False)

	button = gtk.Button(stock = gtk.STOCK_CLOSE)
	button.connect('clicked', self.window.destroy)
	bbox.pack_start(button)
