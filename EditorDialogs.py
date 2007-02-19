# @(#) $Id: StartScreen.py 30 2007-02-11 22:16:26Z balu $
# -*- coding: utf8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import pango

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

class QuestionEditDialog(gtk.Dialog):

    def __init__(self, parent, question = '', answers = ''):
	gtk.Dialog.__init__(
	    self,
	    title = u'Вопрос/ответ',
	    parent = parent,
	    flags = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
	    buttons = (
		'OK и продолжить', gtk.RESPONSE_ACCEPT,
		gtk.STOCK_OK, gtk.RESPONSE_OK,
		gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL
	    )
	)
	self.setContinuable(True)

	table = gtk.Table(3, 2)
	table.set_border_width(10)
	table.set_row_spacings(5)
	table.set_col_spacings(5)
	self.vbox.pack_start(table, True, False)

	label = gtk.Label(u'Вопрос')
	alignment = gtk.Alignment(yalign = 0.5)
	alignment.add(label)
	table.attach(alignment, 0, 1, 0, 1)

	self.questionEntry = gtk.Entry()
	self.questionEntry.set_width_chars(50)
	self.questionEntry.set_activates_default(True)
	table.attach(self.questionEntry, 1, 2, 0, 1)

	label = gtk.Label(u'Ответы')
	alignment = gtk.Alignment(yalign = 0.5)
	alignment.add(label)
	table.attach(alignment, 0, 1, 1, 2)

	self.answersEntry = gtk.Entry()
	self.answersEntry.set_width_chars(50)
	self.answersEntry.set_activates_default(True)
	table.attach(self.answersEntry, 1, 2, 1, 2)

	label = gtk.Label(u'Если допускается несколько вариантов ответа, перечислите их через точку с запятой (;)')
	label.modify_font(pango.FontDescription('8'))
	alignment = gtk.Alignment(yalign = 0.5)
	alignment.add(label)
	table.attach(alignment, 1, 2, 2, 3)

	self.setTask(question, answers)

	table.show_all()

    def getQuestion(self):
	return self.questionEntry.get_text()

    def getAnswer(self):
	return self.answersEntry.get_text()

    def getAnswers(self):
	return [a.strip() for a in self.getAnswer().split(';')]

    def setTask(self, question, answers):
	self.questionEntry.set_text(question)
	self.answersEntry.set_text(answers)
	self.questionEntry.grab_focus()

    def clearTask(self):
	self.setTask('', '')

    def setContinuable(self, continuable):
	if continuable:
	    self.set_response_sensitive(gtk.RESPONSE_ACCEPT, True)
	    self.set_default_response(gtk.RESPONSE_ACCEPT)
	else:
	    self.set_default_response(gtk.RESPONSE_OK)
	    self.set_response_sensitive(gtk.RESPONSE_ACCEPT, False)
