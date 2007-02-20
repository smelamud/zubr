# @(#) $Id: StartScreen.py 30 2007-02-11 22:16:26Z balu $
# -*- coding: utf8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import gobject
from xml import xpath
from xml.dom.minidom import parse
from xml.dom import getDOMImplementation
import xml.parsers.expat

from EditorDialogs import LessonEditDialog, QuestionEditDialog
import AppWindow

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

	accelGroup = gtk.AccelGroup()
	self.add_accel_group(accelGroup)
	self.tooltips = gtk.Tooltips()

	toolbar = gtk.Toolbar()
	toolButton = gtk.ToolButton(gtk.STOCK_NEW)
	toolButton.connect('clicked', self.new)
	toolButton.set_tooltip(self.tooltips, u'Создать новый файл (Ctrl+N)')
	toolButton.add_accelerator('clicked', accelGroup, ord('n'),
		gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE | gtk.ACCEL_LOCKED)
	toolbar.insert(toolButton, -1)
	toolButton = gtk.ToolButton(gtk.STOCK_OPEN)
	toolButton.connect('clicked', self.open)
	toolButton.set_tooltip(self.tooltips, u'Открыть файл (Ctrl+O)')
	toolButton.add_accelerator('clicked', accelGroup, ord('o'),
		gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE | gtk.ACCEL_LOCKED)
	toolbar.insert(toolButton, -1)
	self.saveButton = gtk.ToolButton(gtk.STOCK_SAVE);
	self.saveButton.set_tooltip(self.tooltips,
		u'Сохранить текущий файл (Ctrl+S)')
	self.saveButton.add_accelerator('clicked', accelGroup, ord('s'),
		gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE | gtk.ACCEL_LOCKED)
	self.saveButton.connect('clicked', self.save)
	toolbar.insert(self.saveButton, -1)
	toolButton = gtk.ToolButton(gtk.STOCK_SAVE_AS)
	toolButton.set_tooltip(self.tooltips,
		u'Сохранить текущий файл как... (Shift+Ctrl+S)')
	toolButton.add_accelerator('clicked', accelGroup, ord('s'),
		gtk.gdk.CONTROL_MASK | gtk.gdk.SHIFT_MASK,
		gtk.ACCEL_VISIBLE | gtk.ACCEL_LOCKED)
	toolButton.connect('clicked', self.saveAs)
	toolbar.insert(toolButton, -1)
	toolbar.insert(gtk.SeparatorToolItem(), -1)
	self.playButton = gtk.ToolButton(gtk.STOCK_MEDIA_PLAY)
	self.playButton.connect('clicked', self.play)
	self.playButton.set_tooltip(self.tooltips,
		u'Запустить тренировку (Ctrl+G)')
	self.playButton.add_accelerator('clicked', accelGroup, ord('g'),
		gtk.gdk.CONTROL_MASK, gtk.ACCEL_VISIBLE | gtk.ACCEL_LOCKED)
	toolbar.insert(self.playButton, -1)
	toolbar.insert(gtk.SeparatorToolItem(), -1)
	toolButton = gtk.ToolButton(gtk.STOCK_CLOSE)
	toolButton.connect('clicked', self.close)
	toolButton.set_tooltip(self.tooltips, u'Закрыть редактор')
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
	toolButton.set_tooltip(self.tooltips, u'Создать новый урок (Insert)')
	toolButton.connect('clicked', self.newLesson)
	toolbar.insert(toolButton, -1)
	self.editLessonButton = gtk.ToolButton(gtk.STOCK_EDIT)
	self.editLessonButton.set_tooltip(self.tooltips, u'Переименовать урок')
	self.editLessonButton.connect('clicked', self.editLesson)
	toolbar.insert(self.editLessonButton, -1)
	self.deleteLessonButton = gtk.ToolButton(gtk.STOCK_DELETE)
	self.deleteLessonButton.set_tooltip(self.tooltips,
		u'Удалить урок (Delete)')
	self.deleteLessonButton.connect('clicked', self.deleteLesson)
	toolbar.insert(self.deleteLessonButton, -1)
	toolbar.insert(gtk.SeparatorToolItem(), -1)
	toolButton = gtk.ToolButton(gtk.STOCK_GO_UP)
	toolButton.set_tooltip(self.tooltips,
		u'Передвинуть урок вверх по списку')
	toolbar.insert(toolButton, -1)
	toolButton = gtk.ToolButton(gtk.STOCK_GO_DOWN)
	toolButton.set_tooltip(self.tooltips,
		u'Передвинуть урок вниз по списку')
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
	self.lessonView.connect('key-press-event', self.lessonKeyPressed)
	self.lessonView.get_selection().connect('changed',
	    self.lessonSelectionChanged)
	scroller.add(self.lessonView)

	tbox = gtk.VBox(False)
	listPaned.pack2(tbox, True)

	toolbar = gtk.Toolbar()
	toolbar.set_style(gtk.TOOLBAR_ICONS)
	self.addQuestionButton = gtk.ToolButton(gtk.STOCK_ADD)
	self.addQuestionButton.set_tooltip(self.tooltips,
		u'Добавить новый вопрос (Insert)')
	self.addQuestionButton.connect('clicked', self.addQuestion)
	toolbar.insert(self.addQuestionButton, -1)
	self.editQuestionButton = gtk.ToolButton(gtk.STOCK_EDIT)
	self.editQuestionButton.set_tooltip(self.tooltips, u'Изменить вопрос')
	self.editQuestionButton.connect('clicked', self.editQuestion)
	toolbar.insert(self.editQuestionButton, -1)
	self.deleteQuestionButton = gtk.ToolButton(gtk.STOCK_REMOVE)
	self.deleteQuestionButton.set_tooltip(self.tooltips,
		u'Удалить вопрос (Delete)')
	self.deleteQuestionButton.connect('clicked', self.deleteQuestion)
	toolbar.insert(self.deleteQuestionButton, -1)
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
	column.set_resizable(True)
	self.questionView.append_column(column)
	renderer = gtk.CellRendererText()
	renderer.set_property('editable', True)
	renderer.connect('edited', self.questionEdited, 0)
	column.pack_start(renderer, True)
	column.add_attribute(renderer, 'text', 0)
	column = gtk.TreeViewColumn()
	column.set_title(u'Ответы')
	column.set_resizable(True)
	self.questionView.append_column(column)
	renderer = gtk.CellRendererText()
	renderer.set_property('editable', True)
	renderer.connect('edited', self.questionEdited, 1)
	column.pack_start(renderer, True)
	column.add_attribute(renderer, 'text', 1)
	self.questionView.connect('key-press-event', self.questionKeyPressed)
	self.questionView.get_selection().connect('changed',
	    self.questionSelectionChanged)
	scroller.add(self.questionView)

	self.openFile(filename)

	container.show_all()

    def setExamTitle(self, title):
	if not title:
	    self.set_title(u'Зубр (редактор)')
	else:
	    self.set_title(u'Зубр (редактор) - ' + title)

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
	dialog.set_default_response(gtk.RESPONSE_OK)
	filter = gtk.FileFilter()
	filter.set_name('Exam file')
	filter.add_pattern('*.exam')
	dialog.add_filter(filter)
	result = dialog.run()
	filename = dialog.get_filename()
	dialog.destroy()
	if result == gtk.RESPONSE_OK:
	    self.openFile(filename)

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
	dialog.set_default_response(gtk.RESPONSE_OK)
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

    def play(self, widget):
	window = AppWindow.AppWindow(self.filename)
	window.switchScreen('start')
	window.show()

    def openFile(self, filename):
	if self.changed:
	    dialog = gtk.MessageDialog(
		self,
		gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
		gtk.MESSAGE_WARNING,
		gtk.BUTTONS_YES_NO,
		u'Файл не сохранен. Сохранить?'
	    )
	    result = dialog.run()
	    dialog.destroy()
	    if result == gtk.RESPONSE_YES:
		self.save(None)

	self.lessonStore.clear()
	if self.doc != None:
	    self.doc.unlink()
	    self.doc = None
	self.filename = filename
	if self.filename != None:
	    try:
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
	    except xml.parsers.expat.ExpatError, e:
		dialog = gtk.MessageDialog(
		    self,
		    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
		    gtk.MESSAGE_ERROR,
		    gtk.BUTTONS_OK,
		    str(e)
		)
		dialog.run()
		dialog.destroy()
		self.filename = None
	if self.filename == None:
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
	self.playButton.set_sensitive(self.filename != None)

    def newLesson(self, widget):
	dialog = LessonEditDialog(self)
	result = dialog.run()
	if result == gtk.RESPONSE_OK:
	    title = dialog.getTitle()
	    lesson = self.doc.createElement('lesson')
	    lesson.setAttribute('title', title)
	    self.doc.documentElement.appendChild(lesson)
	    self.lessonStore.append((title, ))
	    self.lessonView.grab_focus()
	    self.lessonView.get_selection() \
		    .select_path(str(len(self.lessonStore) - 1))
	    self.setChanged(True)
	dialog.destroy()

    def getSelectedLesson(self):
	(model, iter) = self.lessonView.get_selection().get_selected()
	if iter == None:
	    lesson = None
	else:
	    lessons = xpath.Evaluate(
		    '//lesson[%s + 1]' % (model.get_string_from_iter(iter)),
		    self.doc
	    )
	    if len(lessons) == 0:
		lesson = None
	    else:
		lesson = lessons[0]
	return (model, iter, lesson)

    def editLesson(self, widget):
	(model, iter, lesson) = self.getSelectedLesson()
	if lesson == None:
	    return
	dialog = LessonEditDialog(self, model.get_value(iter, 0))
	result = dialog.run()
	if result == gtk.RESPONSE_OK:
	    self.renameLesson(dialog.getTitle())
	dialog.destroy()
	self.lessonView.grab_focus()
	self.lessonView.get_selection().select_iter(iter)

    def deleteLesson(self, widget):
	(model, iter, lesson) = self.getSelectedLesson()
	if lesson == None:
	    return
	tasks = xpath.Evaluate('.//task', lesson)
	if len(tasks) > 0:
	    dialog = gtk.MessageDialog(
		self,
		gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
		gtk.MESSAGE_WARNING,
		gtk.BUTTONS_YES_NO,
		u'Вы действительно хотите удалить урок со всем содержимым?'
	    )
	    result = dialog.run()
	    dialog.destroy()
	    if result != gtk.RESPONSE_YES:
		return
	lesson.parentNode.removeChild(lesson)
	lesson.unlink()
	model.remove(iter)
	self.setChanged(True)

    def titleEntryChanged(self, widget):
	exams = xpath.Evaluate('//exam', self.doc)
	assert len(exams) > 0
	exams[0].setAttribute('title', self.titleEntry.get_text())
	self.setChanged(True)

    def lessonTitleEdited(self, widget, path, new_text):
	self.renameLesson(new_text)

    def renameLesson(self, newTitle):
	(model, iter, lesson) = self.getSelectedLesson()
	if lesson == None:
	    return
	model.set_value(iter, 0, newTitle)
	lesson.setAttribute('title', newTitle)
	self.setChanged(True)

    def lessonSelectionChanged(self, param1 = None, param2 = None):
	(model, iter, lesson) = self.getSelectedLesson()
	self.questionStore.clear()
	if lesson != None:
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
	    self.editLessonButton.set_sensitive(True)
	    self.deleteLessonButton.set_sensitive(True)
	    self.addQuestionButton.set_sensitive(True)
	else:
	    self.editLessonButton.set_sensitive(False)
	    self.deleteLessonButton.set_sensitive(False)
	    self.addQuestionButton.set_sensitive(False)
	self.questionSelectionChanged()

    def lessonKeyPressed(self, widget, event):
	if event.keyval == gtk.keysyms.Insert:
	    self.newLesson(widget)
	if event.keyval == gtk.keysyms.Delete:
	    self.deleteLesson(widget)

    def _createTask(self, question, answers):
	task = self.doc.createElement('task')
	qitem = self.doc.createElement('question')
	task.appendChild(qitem)
	qitem.appendChild(self.doc.createTextNode(question))
	for s in answers:
	    aitem = self.doc.createElement('answer')
	    task.appendChild(aitem)
	    aitem.appendChild(self.doc.createTextNode(s))
	return task

    def addQuestion(self, widget):
	(model, iter, lesson) = self.getSelectedLesson()
	dialog = QuestionEditDialog(self)
	while True:
	    dialog.clearTask()
	    result = dialog.run()
	    if result in (gtk.RESPONSE_OK, gtk.RESPONSE_ACCEPT):
		task = self._createTask(dialog.getQuestion(),
			dialog.getAnswers())
		lesson.appendChild(task)
		self.questionStore.append((dialog.getQuestion(),
			dialog.getAnswer()))
		self.setChanged(True)
		self.questionView.grab_focus()
		self.questionView.get_selection().unselect_all()
		path = str(len(self.questionStore) - 1)
		self.questionView.get_selection().select_path(path)
		self.questionView.set_cursor(path)
	    if result != gtk.RESPONSE_ACCEPT:
		break
	dialog.destroy()

    def getSelectedQuestions(self):
	(model, iter, lesson) = self.getSelectedLesson()
	if lesson == None:
	    return (self.questionStore, [], [])
	iters = []
	questions = []
	iter = self.questionStore.get_iter_first()
	tasks = xpath.Evaluate('./task', lesson)
	selection = self.questionView.get_selection()
	for task in tasks:
	    if iter == None:
		break
	    if selection.iter_is_selected(iter):
		iters += [iter]
		questions += [task]
	    iter = self.questionStore.iter_next(iter)
	return (self.questionStore, iters, questions)

    def editQuestion(self, widget):
	(model, iters, questions) = self.getSelectedQuestions()
	if len(questions) <= 0:
	    return
	assert len(iters) == len(questions)
	dialog = QuestionEditDialog(self)
	for i in range(0, len(questions)):
	    iter = iters[i]
	    dialog.setTask(model.get_value(iter, 0), model.get_value(iter, 1))
	    dialog.setContinuable(i < len(questions) - 1)
	    result = dialog.run()
	    if result in (gtk.RESPONSE_OK, gtk.RESPONSE_ACCEPT):
		self.modifyQuestion(dialog.getQuestion(), dialog.getAnswer(),
			dialog.getAnswers(), i)
	    self.questionView.grab_focus()
	    self.questionView.get_selection().select_iter(iter)
	    if result != gtk.RESPONSE_ACCEPT:
		break
	dialog.destroy()

    def deleteQuestion(self, widget):
	(model, iters, questions) = self.getSelectedQuestions()
	if len(questions) <= 0:
	    return
	assert len(iters) == len(questions)
	dialog = gtk.MessageDialog(
	    self,
	    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
	    gtk.MESSAGE_WARNING,
	    gtk.BUTTONS_YES_NO,
	    u'Вы действительно хотите удалить выбранные вопросы (%i)?' \
		    % (len(questions))
	)
	result = dialog.run()
	dialog.destroy()
	if result != gtk.RESPONSE_YES:
	    return
	for (iter, question) in zip(iters, questions):
	    question.parentNode.removeChild(question)
	    question.unlink()
	    model.remove(iter)
	self.setChanged(True)

    def questionEdited(self, widget, path, new_text, column):
	(model, iters, questions) = self.getSelectedQuestions()
	indexes = [i for i in range(0, len(iters))
		if model.get_string_from_iter(iters[i]) == path]
	if len(indexes) <= 0:
	    return
	index = indexes[0]
	if column == 0:
	    newQuestion = new_text
	    newAnswer = self.questionStore[int(path)][1]
	elif column == 1:
	    newQuestion = self.questionStore[int(path)][0]
	    newAnswer = new_text
	else:
	    return
	newAnswers = [a.strip() for a in newAnswer.split(';')]
	self.modifyQuestion(newQuestion, newAnswer, newAnswers, index)

    def modifyQuestion(self, newQuestion, newAnswer, newAnswers, index = 0):
	(model, iters, questions) = self.getSelectedQuestions()
	if len(questions) <= 0:
	    return
	assert len(iters) == len(questions)
	iter = iters[index]
	model.set_value(iter, 0, newQuestion)
	model.set_value(iter, 1, newAnswer)
	task = questions[index]
	newTask = self._createTask(newQuestion, newAnswers)
	task.parentNode.replaceChild(newTask, task)
	task.unlink()
	self.setChanged(True)

    def questionSelectionChanged(self, param1 = None, param2 = None):
	(model, iter, questions) = self.getSelectedQuestions()
	if len(questions) > 0:
	    self.editQuestionButton.set_sensitive(True)
	    self.deleteQuestionButton.set_sensitive(True)
	else:
	    self.editQuestionButton.set_sensitive(False)
	    self.deleteQuestionButton.set_sensitive(False)

    def questionKeyPressed(self, widget, event):
	if event.keyval == gtk.keysyms.Insert \
		and self.addQuestionButton.get_property('sensitive'):
	    self.addQuestion(widget)
