# @(#) $Id: StartScreen.py 30 2007-02-11 22:16:26Z balu $
# -*- coding: utf8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import gobject
from xml import xpath
from xml.dom.minidom import parse
from xml.dom import getDOMImplementation

class EditorWindow(gtk.Window):

    def __init__(self, filename = None):
	gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
	self.running = False
	self.filename = None
	self.doc = None
	self.changed = False

	self.set_position(gtk.WIN_POS_CENTER)
	self.set_resizable(True)
	self.resize(600, 600)
	self.connect('destroy', self.close)

	container = gtk.VBox(False, 5)
	self.add(container)

	toolbar = gtk.Toolbar()
	toolButton = gtk.ToolButton(gtk.STOCK_NEW)
	toolButton.connect('clicked', self.new)
	toolbar.insert(toolButton, -1)
	toolButton = gtk.ToolButton(gtk.STOCK_OPEN)
	toolButton.connect('clicked', self.open)
	toolbar.insert(toolButton, -1)
	self.saveButton = gtk.ToolButton(gtk.STOCK_SAVE);
	self.saveButton.connect('clicked', self.save)
	toolbar.insert(self.saveButton, -1)
	toolButton = gtk.ToolButton(gtk.STOCK_SAVE_AS)
	toolButton.connect('clicked', self.saveAs)
	toolbar.insert(toolButton, -1)
	toolbar.insert(gtk.SeparatorToolItem(), -1)
	toolButton = gtk.ToolButton(gtk.STOCK_CLOSE)
	toolButton.connect('clicked', self.close)
	toolbar.insert(toolButton, -1)
	container.pack_start(toolbar, False)

	fbox = gtk.HBox(False, 5)
	fbox.set_border_width(10)
	container.pack_start(fbox, False)

	label = gtk.Label(u'Название')
	fbox.pack_start(label, False)

	self.titleEntry = gtk.Entry()
	self.titleEntry.connect('changed', self.titleEntryChanged)
	fbox.pack_start(self.titleEntry, True, True)
	self.titleEntry.grab_focus()

	listPaned = gtk.HPaned()
	container.pack_start(listPaned, True, True)

	tbox = gtk.VBox(False)
	listPaned.pack1(tbox, True)

	toolbar = gtk.Toolbar()
	toolbar.set_style(gtk.TOOLBAR_ICONS)
	toolButton = gtk.ToolButton(gtk.STOCK_NEW)
	toolbar.insert(toolButton, -1)
	toolButton = gtk.ToolButton(gtk.STOCK_EDIT)
	toolbar.insert(toolButton, -1)
	toolButton = gtk.ToolButton(gtk.STOCK_DELETE)
	toolbar.insert(toolButton, -1)
	tbox.pack_start(toolbar, False)

	scroller = gtk.ScrolledWindow()
	scroller.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
	tbox.pack_start(scroller, True, True)

	self.lessonStore = gtk.ListStore(gobject.TYPE_STRING)
	self.lessonView = gtk.TreeView(self.lessonStore)
	column = gtk.TreeViewColumn()
	column.set_title(u'Урок')
	self.lessonView.append_column(column)
	renderer = gtk.CellRendererText()
	renderer.set_property('editable', True)
	renderer.connect('edited', self.lessonTitleEdited)
	column.pack_start(renderer, True)
	column.add_attribute(renderer, 'text', 0)
	self.lessonView.get_selection().connect('changed',
	    self.lessonSelectionChanged)
	scroller.add(self.lessonView)

	tbox = gtk.VBox(False)
	listPaned.pack2(tbox, True)

	toolbar = gtk.Toolbar()
	toolbar.set_style(gtk.TOOLBAR_ICONS)
	toolButton = gtk.ToolButton(gtk.STOCK_NEW)
	toolbar.insert(toolButton, -1)
	toolButton = gtk.ToolButton(gtk.STOCK_EDIT)
	toolbar.insert(toolButton, -1)
	toolButton = gtk.ToolButton(gtk.STOCK_DELETE)
	toolbar.insert(toolButton, -1)
	tbox.pack_start(toolbar, False)

	scroller = gtk.ScrolledWindow()
	scroller.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
	tbox.pack_start(scroller, True, True)

	self.questionStore = gtk.ListStore(gobject.TYPE_STRING,
		gobject.TYPE_STRING)
	self.questionView = gtk.TreeView(self.questionStore)
	self.questionView.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
	column = gtk.TreeViewColumn()
	column.set_title(u'Вопрос')
	self.questionView.append_column(column)
	renderer = gtk.CellRendererText()
	renderer.set_property('editable', True)
	column.pack_start(renderer, True)
	column.add_attribute(renderer, 'text', 0)
	column = gtk.TreeViewColumn()
	column.set_title(u'Ответы')
	self.questionView.append_column(column)
	renderer = gtk.CellRendererText()
	renderer.set_property('editable', True)
	column.pack_start(renderer, True)
	column.add_attribute(renderer, 'text', 1)
	scroller.add(self.questionView)

	self.openFile(filename)

	container.show_all()

    def setExamTitle(self, title):
	if not title:
	    self.set_title(u'Зубрёжка (редактор)')
	else:
	    self.set_title(u'Зубрёжка (редактор) - ' + title)

    def run(self):
	self.running = True
	self.show()
	gtk.main()

    def new(self, widget):
	self.openFile(None)

    def open(self, widget):
	dialog = gtk.FileChooserDialog(
		title = u'Открыть файл',
		buttons = (
		    gtk.STOCK_OPEN, gtk.RESPONSE_OK,
		    gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL
		)
	)
	filter = gtk.FileFilter()
	filter.set_name('Exam file')
	filter.add_pattern('*.exam')
	dialog.add_filter(filter)
	result = dialog.run()
	if result == gtk.RESPONSE_OK:
	    self.openFile(dialog.get_filename())
	dialog.destroy()

    def save(self, widget):
	if self.filename == None:
	    self.saveAs(widget)
	else:
	    self.saveFile()

    def saveAs(self, widget):
	dialog = gtk.FileChooserDialog(
		title = u'Сохранить файл',
		action = gtk.FILE_CHOOSER_ACTION_SAVE,
		buttons = (
		    gtk.STOCK_SAVE, gtk.RESPONSE_OK,
		    gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL
		)
	)
	filter = gtk.FileFilter()
	filter.set_name('Exam file')
	filter.add_pattern('*.exam')
	dialog.add_filter(filter)
	dialog.set_do_overwrite_confirmation(True)
	if self.filename != None:
	    dialog.set_filename(self.filename)
	result = dialog.run()
	if result == gtk.RESPONSE_OK:
	    self.filename = dialog.get_filename()
	    self.setExamTitle(self.filename)
	    self.saveFile()
	dialog.destroy()

    def close(self, widget):
	self.openFile(None)
	self.destroy()
	if self.running:
	    gtk.main_quit()

    def openFile(self, filename):
	self.lessonStore.clear()
	self.filename = filename
	if filename != None:
	    self.setExamTitle(filename)
	    self.doc = parse(filename)
	    title = xpath.Evaluate('//exam/@title', self.doc)
	    if len(title) > 0:
		self.titleEntry.set_text(title[0].nodeValue)
	    else:
		self.titleEntry.set_text('')
	    lessons = xpath.Evaluate('//lesson/@title', self.doc)
	    for lesson in lessons:
		self.lessonStore.append((lesson.nodeValue, ))
	else:
	    self.doc = getDOMImplementation().createDocument(None, 'exam', None)
	    self.setExamTitle('')
	    self.titleEntry.set_text('')
	self.lessonSelectionChanged()
	self.setChanged(False)

    def saveFile(self):
	f = file(self.filename, 'w')
	f.write(self.doc.toxml())
	self.setChanged(False)

    def setChanged(self, value):
	self.changed = value
	self.saveButton.set_sensitive(self.changed)

    def titleEntryChanged(self, widget):
	exams = xpath.Evaluate('//exam', self.doc)
	assert len(exams) > 0
	exams[0].setAttribute('title', self.titleEntry.get_text())
	self.setChanged(True)

    def lessonTitleEdited(self, widget, path, new_text):
	self.lessonStore[int(path)][0] = new_text
	lessons = xpath.Evaluate('//lesson[%s + 1]' % path, self.doc)
	assert len(lessons) > 0
	lessons[0].setAttribute('title', new_text)
	self.setChanged(True)

    def lessonSelectionChanged(self, param1 = None, param2 = None):
	(model, iter) = self.lessonView.get_selection().get_selected()
	self.questionStore.clear()
	if iter != None:
	    lessons = xpath.Evaluate(
		    '//lesson[%s + 1]' % (model.get_path(iter)),
		    self.doc
	    )
	    if len(lessons) == 0:
		return
	    else:
		lesson = lessons[0]
	    tasks = xpath.Evaluate('./task', lesson)
	    for task in tasks:
		questions = xpath.Evaluate('./question/text()', task)
		if len(questions) == 0:
		    question = ''
		else:
		    question = questions[0].data
		answers = [a.data for a
				in xpath.Evaluate('./answer/text()', task)]
		self.questionStore.append((question, u';'.join(answers)))
