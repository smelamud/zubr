# @(#) $Id$
# -*- coding: utf8 -*-

class Screen:

    container = None
    window = None

    def __init__(self, window, container):
	self.container = container
	self.window = window

    def show(self):
	self.window.add(self.container)
	self.container.show_all()

    def hide(self):
	self.container.hide_all()
	self.window.remove(self.container)
