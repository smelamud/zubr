# @(#) $Id$
# -*- coding: utf8 -*-

import random

class Question:

    def __init__(self, question = "", answers = [], task = None):
	if task == None:
	    self.question = question
	    if isinstance(answers, str) or isinstance(answers, unicode):
		self.answers = [answers]
	    else:
		self.answers = answers
	else:
	    self.question = task.question
	    self.answers = task.answers
	self.reset()

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

    def __init__(self):
	random.seed()
	self.questions = []
	self.reset()

    def load(self, file, lessons):
	for lesson in file.lessons:
	    if lesson.title in lessons:
		for task in lesson.tasks:
		    self.questions.append(Question(task = task))

    def reset(self):
	self.totalAnswers = 0
	self.rightAnswers = 0
	for q in self.questions:
	    q.reset()

    def ask(self):
	return random.choice(self.questions)

    def answer(self, question, answer):
	self.totalAnswers+=1
	right = question.answer(answer)
	if right:
	    self.rightAnswers+=1
	return right
