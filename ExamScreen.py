# @(#) $Id$
# -*- coding: utf8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import pango
import gobject

from Screen import Screen

class Scoreboard(gtk.VBox):

    def __init__(self, examiner):
	gtk.VBox.__init__(self, True, 0)
	self._answerLine = gtk.Label()
	self._answerLine.set_alignment(0.5, 0)
	self._answerLine.modify_font(pango.FontDescription('12'))
	self.pack_start(self._answerLine, False)

	self._timeLine = gtk.Label()
	self._timeLine.set_alignment(0.5, 0)
	self._timeLine.modify_font(pango.FontDescription('12'))
	self.pack_start(self._timeLine, False)

	self.examiner = examiner
	self.refresh()

    def refresh(self):
	self._answerLine.set_markup(
	    u'<span foreground="#00CC00">%d правильно</span>, ' \
	    u'<span foreground="#FF0000">%d неправильно</span>, ' \
	    u'%d всего' %
	    (self.examiner.rightAnswers,
	     self.examiner.totalAnswers - self.examiner.rightAnswers,
	     self.examiner.totalAnswers))
	self._timeLine.set_markup(
	    u'Среднее время ответа - %d сек (%d сек для последних вопросов)' %
	    (self.examiner.getAverageTime(), self.examiner.getLastTime()))

class ExamScreen(Screen):

    NONE = 0
    RIGHT = 1
    WRONG = 2

    _RIGHT_COLOR = gtk.gdk.Color(0, 0x7FFF, 0)
    _WRONG_COLOR = gtk.gdk.Color(0xBFFF, 0, 0)

    def __init__(self, window):
	Screen.__init__(self, window, gtk.VBox(False, 20))

	self.scoreboard = Scoreboard(window.examiner)
	self.container.pack_start(self.scoreboard, False)

	self.questionLabel = gtk.Label(u'Вопрос')
	self.questionLabel.set_alignment(0, 1)
	self.questionLabel.modify_font(pango.FontDescription('14'))
	self.container.pack_start(self.questionLabel)

	self.resultLabel = gtk.Label()
	self.resultLabel.set_alignment(0, 0)
	self.resultLabel.modify_font(pango.FontDescription('bold 14'))
	self.container.pack_start(self.resultLabel, False)

	hbox = gtk.HBox(False, 2)
	self.container.pack_start(hbox, False)

	self.entry = gtk.Entry()
	self.entry.modify_font(pango.FontDescription('14'))
	self.entry.set_activates_default(True)
	hbox.pack_start(self.entry)

	self.okButton = gtk.Button(stock = gtk.STOCK_OK)
	self.okButton.connect('clicked', self.answer)
	hbox.pack_start(self.okButton, False)

	bbox = gtk.HButtonBox()
	bbox.set_spacing(5)
	bbox.set_layout(gtk.BUTTONBOX_END)
	self.container.pack_start(bbox, False)

	button = gtk.Button(stock = gtk.STOCK_MEDIA_PAUSE)
	button.connect('clicked', self.pause)
	bbox.pack_start(button)

	button = gtk.Button(stock = gtk.STOCK_MEDIA_STOP)
	button.connect('clicked', self.stop)
	bbox.pack_start(button)

	button = gtk.Button(stock = gtk.STOCK_CLOSE)
	button.connect('clicked', self.window.destroy)
	bbox.pack_start(button)

	self.currentQuestion = None

    def showResult(self, result):
	if result == self.RIGHT:
	    text = '; '.join(self.currentQuestion.answers)
	    color = self._RIGHT_COLOR
	elif result == self.WRONG:
	    text = '; '.join(self.currentQuestion.answers)
	    color = self._WRONG_COLOR
	else:
	    text = u''
	    color = self._RIGHT_COLOR
	self.resultLabel.set_text(text)
	self.resultLabel.modify_fg(gtk.STATE_NORMAL, color)

    def ask(self):
	self.currentQuestion = self.window.examiner.ask()
	if self.currentQuestion == None:
	    self.stop()
	    return
	self.questionLabel.set_text(self.currentQuestion.question)
	self.showResult(self.NONE)
	self.entry.set_text("")
	self.entry.set_sensitive(True)
	self.entry.grab_focus()
	self.okButton.set_sensitive(True)
	self.okButton.set_flags(gtk.CAN_DEFAULT)
	self.okButton.grab_default()

    def answer(self, widget, data = None):
	right = self.window.examiner.answer(self.currentQuestion,
	    self.entry.get_text())
	if right:
	    self.showResult(self.RIGHT)
	else:
	    self.showResult(self.WRONG)
	self.entry.set_sensitive(False)
	self.okButton.set_sensitive(False)
	self.scoreboard.refresh()
	if right:
	    timeout = 1000
	else:
	    timeout = 3000
	gobject.timeout_add(timeout, ExamScreen.askNext, self)

    def askNext(self):
	self.ask()
	return False

    def show(self):
	Screen.show(self)
	self.scoreboard.refresh()
	self.window.add_events(gtk.gdk.FOCUS_CHANGE_MASK)
	self.focusHandler = self.window.connect('focus-out-event', self.pause)
	self.ask()

    def hide(self):
	self.window.disconnect(self.focusHandler)
	Screen.hide(self)

    def pause(self, param1 = None, param2 = None):
	self.window.switchScreen('pause')

    def stop(self, widget = None):
	self.window.switchScreen('finish')
