from pyfiglet import Figlet
import os
import drawille
import curses
from PIL import Image
from common import chars
import termglyph

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


def load_letters(dirname):
    res = {}
    for c in chars('az', 'AZ'):
        res[c] = Image.open(os.path.join(dirname, c + '.png'))
    return res


def letterwork(stdscr):
    letter_images = load_letters('out')

    text = 'Long long time ago I started testing this file'
    text_by_word = text.split()
    for word in text_by_word:
        images = [letter_images[letter] for letter in word]

        widths, heights = zip(*(i.size for i in images))
        total_w = sum(widths)
        total_h = sum(heights)

        word_image = Image.new('RGB', (total_w, total_h))
        x_offset = 0
        for im in images:
            word_image.paste(im, (x_offset, 0))
            x_offset += im.size[0]

        termglyph.display(word_image)


if __name__ == '__main__':
#    curses.wrapper(main)
#    curses.wrapper(letterwork)
    letterwork(12)
#    stdscr = curses.initscr()
#    main(12)
