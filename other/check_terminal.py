from typing import Literal

import curses

COLOR_ORANGE = 8


def display_heading(win: curses.window) -> None:
    win.attron(curses.A_STANDOUT)
    win.addstr(2, 22, "ncurses")
    win.attroff(curses.A_STANDOUT)
    win.addstr(2, 22 + len("ncurses"), " Environment Interrogator")
    win.box()
    win.refresh()


def test_color_support(win: curses.window) -> None:
    colors: Literal['YES', 'NO'] = "YES" if curses.has_colors() else "NO"
    win.addstr(2, 5, "Supports color: ")
    if colors == "YES":
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        win.attron(curses.color_pair(1))
    win.addstr(2, 5 + len("Supports color: "), colors)
    if colors == "YES":
        win.attroff(curses.color_pair(1))


def test_change_color_support(win: curses.window) -> None:
    change_color: Literal['YES', 'NO'] = "YES" if curses.can_change_color() else "NO"
    win.addstr(4, 5, "Supports change color: ")
    if change_color == "YES":
        curses.init_color(COLOR_ORANGE, 1000, 500, 0)
        curses.init_pair(2, COLOR_ORANGE, curses.COLOR_BLACK)
        win.attron(curses.color_pair(2))
    win.addstr(4, 5 + len("Supports change color: "), change_color)
    if change_color == "YES":
        win.attroff(curses.color_pair(2))

def display_window_sizes(win0: curses.window, win1: curses.window, win2: curses.window) -> None:
    rows, cols = win0.getmaxyx()
    win2.addstr(6, 5, f"Main window size: {rows} by {cols}")
    win2_rows, win2_cols = win2.getmaxyx()
    win2.addstr(8, 5, f"Current window size: {win2_rows} by {win2_cols}")
    win1_rows, win1_cols = win1.getmaxyx()
    win2.addstr(10, 5, f"Top window size: {win1_rows} by {win1_cols}")
    beg_y, beg_x = win2.getbegyx()
    win2.addstr(12, 5, f"Current window top left pos: {beg_y}, {beg_x}")


def main(stdscr: curses.window) -> None:
    curses.noecho()
    stdscr.refresh()

    win1: curses.window = curses.newwin(5, 76, 1, 2)
    win2: curses.window = curses.newwin(15, 46, 6, 18)

    display_heading(win=win1)
    test_color_support(win=win2)
    test_change_color_support(win=win2)
    display_window_sizes(win0=stdscr, win1=win1, win2=win2)

    win2.box()
    win2.refresh()

    stdscr.addstr(22, 25, "Enter a character to quit: ")
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)