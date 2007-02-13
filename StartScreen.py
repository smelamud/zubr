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
from EditorWindow import EditorWindow

class StartScreen(Screen):

    def __init__(self, window):
	Screen.__init__(self, window, gtk.VBox(False, spacing = 5))
	self.examiner = window.examiner

	fbox = gtk.HBox(False, 5)
	self.container.pack_start(fbox, False)

	label = gtk.Label(u'Файл с вопросами')
	fbox.pack_start(label, False)

	self.file = gtk.FileChooserButton('Файл с вопросами')
	filter = gtk.FileFilter()
	filter.set_name('Exam file')
	filter.add_pattern('*.exam')
	self.file.add_filter(filter)
	self.file.connect('selection-changed', self.fileChanged)
	fbox.pack_start(self.file, True, True)

	self.editButton = gtk.Button(stock = gtk.STOCK_EDIT)
	self.editButton.connect('clicked', self.edit)
	fbox.pack_start(self.editButton, False)

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
	column.set_resizable(True)
	self.questionView.append_column(column)
	renderer = gtk.CellRendererText()
	column.pack_start(renderer, True)
	column.add_attribute(renderer, 'text', 0)
	column = gtk.TreeViewColumn()
	column.set_title(u'Ответы')
	column.set_resizable(True)
	self.questionView.append_column(column)
	renderer = gtk.CellRendererText()
	column.pack_start(renderer, True)
	column.add_attribute(renderer, 'text', 1)
	scroller.add(self.questionView)

	hbox = gtk.HBox(False, 5)
	self.container.pack_start(hbox, False)

	hbox.pack_start(gtk.Label(u'Вопрос считается зазубренным после'), False)
	self.answerCount = gtk.combo_box_new_text()
	for item in [1, 2, 3, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100, u'\u221e']:
	    self.answerCount.append_text(str(item))
	self.answerCount.set_active(3)
	self.answerCount.connect('changed', self.answerCountChanged)
	hbox.pack_start(self.answerCount, False)
	hbox.pack_start(gtk.Label(u'правильных ответов'), False)

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

    def edit(self, widget):
	editor = EditorWindow(self.file.get_filename())
	editor.show()

    def fileChanged(self, filechooser = None):
	filename = self.file.get_filename()
	self.lessonStore.clear()
	if filename != None:
	    self.examTree = parse(filename)
	    title = xpath.Evaluate('//exam/@title', self.examTree)
	    if len(title) > 0:
		self.window.setExamTitle(title[0].nodeValue)
	    else:
		self.window.setExamTitle('')
	    lessons = xpath.Evaluate('//lesson/@title', self.examTree)
	    for lesson in lessons:
		self.lessonStore.append((lesson.nodeValue, ))
	else:
	    self.window.setExamTitle('')
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
		self.questionStore.append((q.question, u';'.join(q.answers)))
	else:
	    self.playButton.set_sensitive(False)

    def answerCountChanged(self, widget):
	text = self.answerCount.get_active_text()
	if text == None:
	    value = 0
	else:
	    try:
		value = int(text)
	    except ValueError:
		value = 0
	self.examiner.maxRightAnswers = value
