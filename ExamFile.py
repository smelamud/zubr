# @(#) $Id$
# -*- coding: utf8 -*-

from xml.dom.minidom import parse
from xml.dom import Node

class Task:
 
    def __init__(self):
	self.question = ""
	self.answers = []

class Lesson:

    def __init__(self, title = ""):
	self.title = title
	self.tasks = []

class ExamFile:

    def __init__(self, filename):
	self.lessons = []
	self._parseTree(parse(filename))

    def _parseTree(self, treeNode):
	for node in treeNode.getElementsByTagName('lesson'):
	    self.lessons.append(self._parseLesson(node))

    def _parseLesson(self, lessonNode):
	lesson = Lesson(lessonNode.getAttribute('title'))
	for node in lessonNode.getElementsByTagName('task'):
	    lesson.tasks.append(self._parseTask(node))
	return lesson

    def _parseTask(self, taskNode):
	task = Task()
	qNodes = taskNode.getElementsByTagName('question')
	if len(qNodes) > 0:
	    task.question = self._textValue(qNodes[0])
	for node in taskNode.getElementsByTagName('answer'):
	    answer = self._textValue(node)
	    if answer:
		task.answers.append(answer)
	return task

    def _textValue(self, element):
	for node in element.childNodes:
	    if node.nodeType == Node.TEXT_NODE:
		return node.data
	return ''
