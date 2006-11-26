# @(#) $Id$
# -*- coding: utf8 -*-

from random import seed, choice

class Question:

    question = ""
    answers = []

    def __init__(self, question, answers):
	self.question = question
	if isinstance(answers, str) or isinstance(answers, unicode):
	    self.answers = [answers]
	else:
	    self.answers = answers
    
    def answer(self, answer):
	return answer in self.answers

class Examiner:

    questions = []

    def __init__(self):
	seed()

	self.questions = [
	    Question(u'Создание государства Израиль', u'1948'),
	    Question(u'Синайская кампания', u'1956'),
	    Question(u'Шестидневная война', u'1967'),
	    Question(u'Война Судного дня', u'1973'),
	    Question(u'Ливанская война (операция "Мир Галилее")', u'1982'),
	]

    def ask(self):
	return choice(self.questions)

    def answer(self, question, answer):
	return question.answer(answer)
