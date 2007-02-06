# @(#) $Id$
# -*- coding: utf8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import gobject
import pango
from xml.dom.minidom import parse
from xml import xpath

from Screen import Screen

class StartScreen(Screen):

    def __init__(self, window):
	Screen.__init__(self, window, gtk.VBox(False, spacing = 5))
	self.examiner = window.examiner

	fbox = gtk.HBox(False)
	self.container.pack_start(fbox, False)

	label = gtk.Label(u'Файл с вопросами')
	fbox.pack_start(label, False, padding = 5)

	self.file = gtk.FileChooserButton('Файл с вопросами')
	filter = gtk.FileFilter()
	filter.set_name('Exam file')
	filter.add_pattern('*.exam')
	self.file.add_filter(filter)
	self.file.connect('selection-changed', self.fileChanged)
	fbox.pack_start(self.file, True, True)

	self.listStore = gtk.ListStore(gobject.TYPE_STRING)
	self.listView = gtk.TreeView(self.listStore)
	self.container.pack_start(self.listView, True, True)

	bbox = gtk.HButtonBox()
	bbox.set_spacing(5)
	bbox.set_layout(gtk.BUTTONBOX_END)
	self.container.pack_start(bbox, False)

	self.playButton = gtk.Button(stock = gtk.STOCK_MEDIA_PLAY)
	self.playButton.connect('clicked', self.start)
	self.fileChanged()
	bbox.pack_start(self.playButton)

	button = gtk.Button(stock = gtk.STOCK_CLOSE)
	button.connect('clicked', self.window.destroy)
	bbox.pack_start(button)

    def start(self, widget, data = None):
	self.window.switchScreen('exam')

    def fileChanged(self, filechooser = None):
	filename = self.file.get_filename()
	if filename != None:
	    tree = parse(filename)
	    lessons = xpath.Evaluate('//lesson/@title', tree)
	    for lesson in lessons:
		self.listStore.append((lesson.nodeValue, ))
	    self.playButton.set_sensitive(True)
	    self.examiner.load(filename, u'Войны')
	else:
	    self.playButton.set_sensitive(False)
