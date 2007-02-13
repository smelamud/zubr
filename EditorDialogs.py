# @(#) $Id: StartScreen.py 30 2007-02-11 22:16:26Z balu $
# -*- coding: utf8 -*-

import pygtk
pygtk.require('2.0')
import gtk

class LessonEditDialog(gtk.Dialog):

    def __init__(self, parent, title = ''):
	gtk.Dialog.__init__(
	    self,
	    title = u'Урок',
	    parent = parent,
	    flags = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
	    buttons = (
		gtk.STOCK_OK, gtk.RESPONSE_OK,
		gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL
	    )
	)
	self.set_default_response(gtk.RESPONSE_OK)

	hbox = gtk.HBox(False, 5)
	hbox.set_border_width(10)
	self.vbox.pack_start(hbox, True, False)

	label = gtk.Label(u'Название урока')
	hbox.pack_start(label, False)

	self.entry = gtk.Entry()
	self.entry.set_width_chars(50)
	self.entry.set_text(title)
	self.entry.set_activates_default(True)
	hbox.pack_start(self.entry, True, True)

	hbox.show_all()

    def getTitle(self):
	return self.entry.get_text()
