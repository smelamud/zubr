# @(#) $Id$
# -*- coding: utf8 -*-

import random

class Question:

    question = ""
    answers = []

    rightAnswers = 0
    totalAnswers = 0

    def __init__(self, question, answers):
	self.question = question
	if isinstance(answers, str) or isinstance(answers, unicode):
	    self.answers = [answers]
	else:
	    self.answers = answers
    
    def reset(self):
	self.totalAnswers = 0
	self.rightAnswers = 0

    def answer(self, answer):
	self.totalAnswers+=1
	right = answer in self.answers
	if right:
	    self.rightAnswers+=1
	return right

class Examiner:

    questions = []

    rightAnswers = 0
    totalAnswers = 0

    def __init__(self):
	random.seed()

	self.questions = [
	    Question(u'Создание государства Израиль', u'1948'),
	    Question(u'Синайская кампания', u'1956'),
	    Question(u'Шестидневная война', u'1967'),
	    Question(u'Война Судного дня', u'1973'),
	    Question(u'Ливанская война (операция "Мир Галилее")', u'1982'),
	]

    def reset(self):
	self.totalAnswers = 0
	self.rightAnswers = 0
	for q in questions:
	    q.reset()

    def ask(self):
	return random.choice(self.questions)

    def answer(self, question, answer):
	self.totalAnswers+=1
	right = question.answer(answer)
	if right:
	    self.rightAnswers+=1
	return right
