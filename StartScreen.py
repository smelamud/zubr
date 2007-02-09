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

	self.listPaned = gtk.HPaned()
	self.container.pack_start(self.listPaned, True, True)

	scroller = gtk.ScrolledWindow()
	scroller.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
	self.listPaned.pack1(scroller, True)

	self.lessonStore = gtk.ListStore(gobject.TYPE_STRING)
	self.lessonView = gtk.TreeView(self.lessonStore)
	self.lessonView.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
	column = gtk.TreeViewColumn()
	column.set_title(u'Урок')
	self.lessonView.append_column(column)
	renderer = gtk.CellRendererText()
	column.pack_start(renderer, True)
	column.add_attribute(renderer, 'text', 0)
	self.lessonView.get_selection().connect('changed',
	    self.lessonSelectionChanged)
	scroller.add(self.lessonView)

	scroller = gtk.ScrolledWindow()
	scroller.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
	self.listPaned.pack2(scroller, True)

	self.questionStore = gtk.ListStore(gobject.TYPE_STRING,
		gobject.TYPE_STRING)
	self.questionView = gtk.TreeView(self.questionStore)
	column = gtk.TreeViewColumn()
	column.set_title(u'Вопрос')
	self.questionView.append_column(column)
	renderer = gtk.CellRendererText()
	column.pack_start(renderer, True)
	column.add_attribute(renderer, 'text', 0)
	column = gtk.TreeViewColumn()
	column.set_title(u'Ответы')
	self.questionView.append_column(column)
	renderer = gtk.CellRendererText()
	column.pack_start(renderer, True)
	column.add_attribute(renderer, 'text', 1)
	scroller.add(self.questionView)

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

    def show(self):
	Screen.show(self)

    def start(self, widget, data = None):
	self.examiner.reset()
	self.window.switchScreen('exam')

    def fileChanged(self, filechooser = None):
	filename = self.file.get_filename()
	self.lessonStore.clear()
	if filename != None:
	    self.examTree = parse(filename)
	    lessons = xpath.Evaluate('//lesson/@title', self.examTree)
	    for lesson in lessons:
		self.lessonStore.append((lesson.nodeValue, ))
	self.lessonSelectionChanged()
    
    def lessonSelectionChanged(self, param1 = None, param2 = None):
	n = self.lessonView.get_selection().count_selected_rows()
	self.questionStore.clear()
	if n > 0:
	    self.playButton.set_sensitive(True)
	    sels = self.lessonView.get_selection().get_selected_rows()[1]
	    lessons = [self.lessonStore[row][0] for row in sels]
	    self.examiner.load(self.examTree, lessons)
	    for q in self.examiner.questions:
		self.questionStore.append((q.question, q.answers[0]))
	else:
	    self.playButton.set_sensitive(False)
