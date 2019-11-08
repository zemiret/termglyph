from pyfiglet import Figlet
import drawille
import curses

def render_title(title):
    f = Figlet(font='starwars')
    a = f.renderText(title.upper())
    a = a.split('\n')
    
    return a


def get_cords(title, w, h):
    title_w = max(map(lambda x: len(x), title))
    title_h = len(title) 

    x, y = 0, 0

    if title_w < w:
        x = (w - title_w) // 2
    if title_h < h:
        y = (h - title_h) // 2

    return x, y


def add_title(stdscr, title, x, y):
    for i, line in enumerate(title):
        stdscr.addstr(y + i, x, line, curses.color_pair(1))


def main(stdscr):
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    title = 'welcome-component.js'

    stdscr.clear()

    # Title
    w, h = drawille.getTerminalSize() 
    rendered = render_title(title)
    x, y = get_cords(rendered, w, h)

    add_title(stdscr, rendered, x, y)

    stdscr.refresh()
    stdscr.getkey()


def letterwork(stdscr):
    pass


if __name__ == '__main__':
#    curses.wrapper(main)
    curses.wrapper(letterwork)
#    stdscr = curses.initscr()
#    main(12)
