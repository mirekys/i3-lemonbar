#!/usr/bin/env python3

import os
import sys
import time
import i3ipc
from signal import SIGTERM
from threading import Thread
from subprocess import Popen, PIPE, check_output
from i3_lemonbar_conf import *

class LemonBar(object):

	def __init__(self, i3):
		self.i3              = i3
		self.focusedWinTitle = self.i3.get_tree().find_focused().name

	def on_window_title_change(self, caller, e):
		self.focusedWinTitle = e.container.name
		self.render()

	def render_workspaces(self, display):
		wsp_icon = "%%{F%s B%s} %%{T2}%s%%{T1}" % (color_back, color_head, icon_wsp)
		wsp_items = ''
		for wsp in self.i3.get_workspaces():
			wsp_name = wsp['name']
			wsp_action = "%%{A:i3-msg workspace %s}" % wsp_name
			if wsp['output'] != display and not wsp['urgent']:
				continue
			if wsp['focused']:
				# Possibly add dark red tint if urgent
				wsp_items += "%%{F%s B%s}%s%s%%{F%s B%s T1} %s %%{F%s B%s}%s%%{A}" % (color_head,
					color_wsp, sep_right, wsp_action, color_back, color_wsp, wsp_name,
					color_wsp, color_head, sep_right)
			elif wsp['urgent']:
				wsp_items += "%%{F%s B%s}%s%s%%{F%s B%s T1} %s %%{F%s B%s}%s%%{A}" % (color_head,
					color_mail, sep_right, wsp_action, color_back, color_mail, wsp_name,
					color_mail, color_head, sep_right)	
			else:
				wsp_items += "%s%%{F%s T1} %s%%{A} " % (wsp_action, color_disable, wsp_name)
		return '%s%s' % (wsp_icon, wsp_items)

	def render_focused_title(self):
		return "%%{F%s B%s}%s%%{F%s B%s T2} %s %%{F%s B-}%s%%{F- B- T1} %s" % (color_head,
			color_sec_b2, sep_right, color_head, color_sec_b2, icon_prog, color_sec_b2,
			sep_right, self.focusedWinTitle)

	def render_datetime(self):
		cdate = "%%{F%s}%s%%{F%s B%s} %%{T2}%s%%{F- T1} %s" % (color_sec_b1, sep_left,
			color_icon, color_sec_b1, icon_clock, time.strftime("%d.%m.%Y"))
		ctime = "%%{F%s}%s%%{F%s B%s} %s %%{F- B-}" % (color_head, sep_left, color_back,
			color_head, time.strftime("%H.%M.%S"))
		return "%s%s%s" % (cdate, stab, ctime)

	def render(self, caller=None, e=None):
		# Render one bar per each output
		out = ''
		for idx,output in enumerate([ out.name for out in self.i3.get_outputs() if out['active'] ]):
			out += "%%{S%d}%%{l}%s%s%%{r}%s" % (idx,
				self.render_workspaces(display=output),
				self.render_focused_title(),
				self.render_datetime()
			)
		print(out)
		sys.stdout.flush()

def shutdown(caller):
	lemonpid=int(check_output('pidof -s lemonbar', shell=True))
	if lemonpid:
		os.kill(lemonpid, SIGTERM)
	sys.exit(0)

def run():
	i3 = i3ipc.Connection()
	i3thread = Thread(target=i3.main)
	lemonbar = LemonBar(i3)
	lemonbar.render()

	i3.on('workspace::focus', lemonbar.render)
	i3.on('window::title',    lemonbar.on_window_title_change)
	i3.on('window::focus',    lemonbar.on_window_title_change)
	i3.on('window::urgent',   lemonbar.render)
	i3.on('ipc-shutdown',     shutdown)

	i3thread.start()
