from pyfiglet import Figlet
import os
import numpy
import drawille
import curses
from PIL import Image
from common import chars
import termglyph
import locale
import time

locale.setlocale(locale.LC_ALL, '')    # set your locale
SWIPE_RATE = 0.01


class FrameLine:
    def __init__(self, frame, y, screen_w, screen_h):
        self.frame = frame 
        self.frame_lines = frame.split('\n')
        self.y = y
        self.screen_w = screen_w
        self.screen_h = screen_h

        self.frame_h = len(self.frame_lines)

    def advance(self):
        self.y -= 1

    def is_partialy_out_down(self):
        return self.y + self.frame_h > self.screen_h

    def is_partialy_out_up(self):
        return self.y < 0 

    def is_out(self):
        return self.y + self.frame_h < 0 or \
                self.y > self.screen_h

    def get_frame(self):
        if self.is_out():
            return ''
        elif self.is_partialy_out_up():
            return '\n'.join(self.frame_lines[abs(self.y):])
        elif self.is_partialy_out_down():
            return '\n'.join(self.frame_lines[:self.screen_h - self.y])
        else:
            return self.frame

    def is_running(self):
        return not self.is_out() and \
                self.y + self.frame_h < self.screen_h

    def can_push_next(self):
        return self.y + self.frame_h + 1 < self.screen_h


def render_title(title):
    f = Figlet(font='starwars')
    a = f.renderText(title.upper())
    a = a.split('\n')
    
    return a


def get_title_cords(title, w, h):
    title_w = max(map(lambda x: len(x), title))
    title_h = len(title) 

    return get_centered_cords(title_w, title_h, w, h)


def get_frame_starting_cords(frame, w, h):
    frame_w = max(map(lambda x: len(x), frame.split('\n')))

    x = 0
    y = h - 1 

    if frame_w < w:
        x = (w - frame_w) // 2
    if y < 0:
        y = 0

    return x, y


def fill_frame_to_x(x, frame):
    fill_str = ' ' * (x + 1)
    frame = '\n'.join(map(lambda x: fill_str + x, frame.split('\n')))

    return frame


def get_centered_cords(text_w=0, text_h=0, w=0, h=0):
    x, y = 0, 0

    if text_w < w:
        x = (w - text_w) // 2
    if text_h < h:
        y = (h - text_h) // 2

    return x, y


def add_title(stdscr, title, x, y):
    for i, line in enumerate(title):
        stdscr.addstr(y + i, x, line, curses.color_pair(1))



def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = numpy.matrix(matrix, dtype=numpy.float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)


def load_letters(dirname):
    res = {}
    for c in chars('az', 'AZ'):
        res[c] = Image.open(os.path.join(dirname, c + '.png'))
    return res


def convert_text_to_bitmaps(text):
    letter_images = load_letters('out')

    text_images = []
    text_by_word = text.split()

    width_lean = 30
    fixed_height = 50

    for word in text_by_word:
        images = [letter_images[letter] for letter in word]

        widths, heights = zip(*(i.size for i in images))
        total_w = sum(widths)
        total_h = max(heights)

        word_image = Image.new('RGB', (total_w, total_h))
        x_offset = 0
        for im in images:
            word_image.paste(im, (x_offset, 0))
            x_offset += im.size[0]

        
        coeffs = find_coeffs(
            [
                (min (total_w // 2, width_lean), 0),
                (total_w -  min(width_lean, total_w // 2), 0),
                (0, fixed_height),
                (total_w, fixed_height)
            ],
            [(0, 0), (total_w, 0), (0, total_h), (total_w, total_h)]
        )

        word_image = word_image.transform(
            (total_w, total_h),
            Image.PERSPECTIVE,
            coeffs,
            Image.BICUBIC)

        text_images.append(word_image)

    return text_images


def draw_title(stdscr, title, w, h):
    rendered = render_title(title)
    x, y = get_title_cords(rendered, w, h)

    add_title(stdscr, rendered, x, y)

    stdscr.refresh()
    stdscr.getkey()


def draw_and_advance_frames(stdscr, frame_window):
    for active_frame in frame_window:
        if active_frame.is_partialy_out_up():
            stdscr.addstr(0, 0, active_frame.get_frame().encode('utf-8'))
        else:
            stdscr.addstr(
                active_frame.y,
                0,
                active_frame.get_frame().encode('utf-8')
            )

        active_frame.advance()


def main(stdscr):
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    title = 'welcome-component.js'

    text = 'abc kanapecki what what the heck is this kurdebele lemme go slower'
#    text = 'abc'
    w, h = drawille.getTerminalSize() 

    stdscr.clear()

    # Title
    draw_title(stdscr, title, w, h)

    # Text 
    word_images = convert_text_to_bitmaps(text)

    frames = map(lambda im: termglyph.get_frame(im, color=False), word_images)
    framelines = []
    for frame in frames:
        x, y = get_frame_starting_cords(frame, w, h)
        frame = fill_frame_to_x(x, frame)

        framelines.append(FrameLine(frame, y, w, h))

    if len(framelines) == 0:
        return

    frame_window = [framelines[0]] 
    frame_index = 1

    while not len(frame_window) == 0:
        stdscr.clear()
        draw_and_advance_frames(stdscr, frame_window)

        if frame_window[0].is_out():
            frame_window.pop(0)

        # TODO: Some error here
        if frame_window[-1].can_push_next() and frame_index < len(framelines):
            frame_window.append(framelines[frame_index])
            frame_index += 1


        stdscr.refresh()
        # stdscr.getkey()
        time.sleep(SWIPE_RATE)
           

if __name__ == '__main__':
    curses.wrapper(main)
