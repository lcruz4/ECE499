import curses
from AX12 import *

def wasd():
  stdscr = curses.initscr()
  curses.noecho()
  curses.cbreak()
  stdscr.keypad(1)
  for i in range(1):
    c = stdscr.getch()
    if c == curses.KEY_UP:
      curses.nocbreak()
      stdscr.keypad(0)
      curses.echo()
      curses.endwin()
      return [0x3FF,0x3FF]
    elif c == curses.KEY_DOWN:
      curses.nocbreak()
      stdscr.keypad(0)
      curses.echo()
      curses.endwin()
      return [-0x3FF,-0x3FF]
    elif c == curses.KEY_RIGHT:
      curses.nocbreak()
      stdscr.keypad(0)
      curses.echo()
      curses.endwin()
      return [0x3FF,-0x3FF]
    elif c == curses.KEY_LEFT:
      curses.nocbreak()
      stdscr.keypad(0)
      curses.echo()
      curses.endwin()
      return [-0x3FF,0x3FF]
    elif c == 'b':
      curses.nocbreak()
      stdscr.keypad(0)
      curses.echo()
      curses.endwin()
      return [0x0,0x0]
    elif c == curses.KEY_HOME:
      curses.nocbreak()
      stdscr.keypad(0)
      curses.echo()
      curses.endwin()
      return -1
  curses.nocbreak()
  stdscr.keypad(0)
  curses.echo()
  curses.endwin()
  return [0x0,0x0]
