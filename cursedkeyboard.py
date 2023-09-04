#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""CursedKeyboard позволит вам узнать скорость вашего набора текста на клавиатуре
Copyright (c) 2023 Okulus Dev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
import curses
from curses import wrapper
from time import time, sleep
from random import choice


def start_screen(stdscr):
	stdscr.clear()
	stdscr.addstr("Добро пожаловать в Проклятую Клавиатуру!")
	stdscr.addstr("\nНажми любую кнопку чтобы начать!")
	stdscr.refresh()
	stdscr.getkey()


def display_text(stdscr, target, current, wpm=0):
	stdscr.addstr(target)
	stdscr.addstr(1, 0, f"\n\nWPM: {wpm}")

	for i, char in enumerate(current):
		correct_char = target[i]
		color = curses.color_pair(1)
		if char != correct_char:
			color = curses.color_pair(2)

		stdscr.addstr(0, i, char, color)


def load_text():
	with open("text.txt", "r") as f:
		lines = f.readlines()
		return choice(lines).strip()


def wpm_test(stdscr):
	target_text = load_text()
	current_text = []
	wpm = 0
	start_time = time()
	stdscr.nodelay(True)

	while True:
		time_elapsed = max(time() - start_time, 1)
		wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

		stdscr.clear()
		display_text(stdscr, target_text, current_text, wpm)
		stdscr.refresh()

		if "".join(current_text) == target_text:
			stdscr.nodelay(False)
			break

		try:
			key = stdscr.getkey()
		except:
			continue

		if key in ("KEY_BACKSPACE", '\b', "\x7f"):
			if len(current_text) > 0:
				current_text.pop()
		elif len(current_text) < len(target_text):
			current_text.append(key)


def main(stdscr):
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

	start_screen(stdscr)

	while True:
		wpm_test(stdscr)

if __name__ == "__main__":
	wrapper(main)
