# @(#) $Id$
# -*- coding: utf8 -*-

import random
import time
from xml.dom.minidom import parse
from xml import xpath

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
	self.maxRightAnswers = 3
	self.questions = []
	self.reset()

    def load(self, filename, lessons):
	tree = parse(filename)
	tasks = xpath.Evaluate('//task', tree)
	for task in tasks:
	    questions = xpath.Evaluate('./question/text()', task)
	    if len(questions) == 0:
		continue
	    question = questions[0].data
	    answers = [a.data for a in xpath.Evaluate('./answer/text()', task)]
	    self.questions.append(Question(question, answers))
	self.reset()

    def reset(self):
	self.totalAnswers = 0
	self.rightAnswers = 0
	for q in self.questions:
	    q.reset()
	self.questionMap = [self.questions[:]]
	self.totalTime = 0
	self.lastTime = []

    def ask(self):
	while len(self.questionMap) > 0 and len(self.questionMap[0]) == 0:
	    del self.questionMap[0]
	if len(self.questionMap) == 0:
	    return None
	question = random.choice(self.questionMap[0])
	question.startTime = int(time.time())
	return question

    def answer(self, question, answer):
	self.totalAnswers+=1
	right = question.answer(answer)
	if right:
	    self.rightAnswers+=1
	dur = int(time.time()) - question.startTime
	self.totalTime += dur
	self.lastTime.append(dur)
	if len(self.lastTime) > len(self.questions):
	    del self.lastTime[0]
	self.moveDown(question)
	return right

    def moveDown(self, question):
	self.questionMap[0].remove(question)
	if self.maxRightAnswers > 0 \
	    and question.rightAnswers < self.maxRightAnswers:
	    while len(self.questionMap) < question.rightAnswers + 2:
		self.questionMap.append([])
	    self.questionMap[question.rightAnswers + 1].append(question)

    def getAverageTime(self):
	if self.totalAnswers == 0:
	    return 0
	else:
	    return int(self.totalTime / self.totalAnswers)

    def getLastTime(self):
	if len(self.lastTime) == 0:
	    return 0
	else:
	    return int(sum(self.lastTime) / len(self.lastTime))

    def printMap(self):
	print '['
	for line in self.questionMap:
	    print ' [',
	    for q in line:
		print '"%s",' % (q.question),
	    print ' ]'
	print ']'
