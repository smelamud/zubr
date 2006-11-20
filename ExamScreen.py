# @(#) $Id$
# -*- coding: utf8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import pango

from Screen import Screen

class ExamScreen(Screen):

    def __init__(self, window):
	Screen.__init__(self, window, gtk.Table(4, 2, True))

	self.container.set_row_spacings(10)
	self.container.set_col_spacings(10)

	label = gtk.Label(u'Вопрос')
	self.container.attach(self._boxed(label), 0, 1, 0, 1)

	label = gtk.Label(u'Верно')
	label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color(0, 32767, 0))
	label.modify_font(pango.FontDescription('bold'))
	self.container.attach(self._boxed(label), 0, 1, 1, 2)

	entry = gtk.Entry()
	self.container.attach(entry, 0, 2, 2, 3)

	label = gtk.Label()
	label.set_markup(u'<span foreground="#00CC00">0</span>/' \
	    u'<span foreground="#FF0000">2</span>/3\n23 сек')
	label.set_justify(gtk.JUSTIFY_RIGHT)
	label.set_line_wrap(True)
	self.container.attach(self._boxed(label, right = True), 1, 2, 0, 2)

	button = gtk.Button(stock = gtk.STOCK_CLOSE)
	button.connect('clicked', self.window.destroy)
	box = gtk.HButtonBox()
	box.set_layout(gtk.BUTTONBOX_END)
	box.pack_start(button)
	self.container.attach(box, 0, 2, 3, 4)

    def _boxed(self, widget, right = False):
	vbox = gtk.VBox(False)
	vbox.pack_start(widget, False, False)
	hbox = gtk.HBox(False)
	if not right:
	    hbox.pack_start(vbox, False, False)
	else:
	    hbox.pack_end(vbox, False, False)
	return hbox
