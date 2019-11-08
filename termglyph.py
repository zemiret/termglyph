import drawille
import argparse
from collections import defaultdict
from PIL import Image
import sys


COLOR_CONVERSION_RATIO = 2**8 // 5


def get_color_string(text, color):
    format_f = lambda text, color: "\33[38;5;" + str(color) + "m" + text + "\33[0m"

    if color >= 0:
        return format_f(text, color)
    else:
        return text


def get_rgb(pix):
    if len(pix) == 1:
        return pix[0], pix[0], pix[0]
    elif len(pix) == 2:
        return pix[0], pix[1], 0

    return pix[0], pix[1], pix[2]


def convert_rgb_to_666(pix_color):
    r, g, b = pix_color
    r = r // COLOR_CONVERSION_RATIO 
    g = g // COLOR_CONVERSION_RATIO
    b = b // COLOR_CONVERSION_RATIO

    return 16 + r * 36  + g * 6 + b


def resize_to_fit(im):
    term_w, term_h = drawille.getTerminalSize()
    term_w *= drawille.X_SIZE_RATIO 
    term_h *= drawille.Y_SIZE_RATIO 
    im_width, im_height = im.size
     
    w_ratio = im_width / term_w 
    h_ratio = im_height / term_h

    ratio = w_ratio if w_ratio > h_ratio else h_ratio
    if ratio > 1:
        new_width = int(im_width // ratio)
        new_height = int(im_height // ratio)

        im = im.resize((new_width, new_height))

    return im



class ImgCanvas(drawille.Canvas):
    def __init__(self, image, *args, **kwargs):
        """
        :param image PIL loaded image (png format for now)
        """

        super().__init__(*args, **kwargs)
        self.image = image
        self.px = image.load()

    def clear(self):
        super().clear()
        self.colors = defaultdict(drawille.intdefaultdict)

    def set(self, x, y, color=(0, 0, 0)):
        """Set a pixel of the :class:`Canvas` object.
        :param x: x coordinate of the pixel
        :param y: y coordinate of the pixel
        """
        x = drawille.normalize(x)
        y = drawille.normalize(y)
        col, row = drawille.get_pos(x, y)

        if type(self.chars[row][col]) != int:
            return

        self.chars[row][col] |= drawille.pixel_map[y % 4][x % 2]
        self.colors[row][col] = convert_rgb_to_666(color) 

    def rows(self, min_x=None, min_y=None, max_x=None, max_y=None):
        """Returns a list of the current :class:`Canvas` object lines.

        :param min_x: (optional) minimum x coordinate of the canvas
        :param min_y: (optional) minimum y coordinate of the canvas
        :param max_x: (optional) maximum x coordinate of the canvas
        :param max_y: (optional) maximum y coordinate of the canvas
        """

        if not self.chars.keys():
            return []

        minrow = min_y // 4 if min_y != None else min(self.chars.keys())
        maxrow = (max_y - 1) // 4 if max_y != None else max(self.chars.keys())
        mincol = min_x // 2 if min_x != None else min(min(x.keys()) for x in self.chars.values())
        maxcol = (max_x - 1) // 2 if max_x != None else max(max(x.keys()) for x in self.chars.values())
        ret = []

        i = 0

        for rownum in range(minrow, maxrow+1):
            if not rownum in self.chars:
                ret.append('')
                continue

            maxcol = (max_x - 1) // 2 if max_x != None else max(self.chars[rownum].keys())
            row = []

            for x in  range(mincol, maxcol+1):
                char = self.chars[rownum].get(x)
                color = self.colors[rownum].get(x)

                if not char:
                    row.append(drawille.unichr(drawille.braille_char_offset))
                elif type(char) != int:
                    row.append(char)
                else:
                    color_string = get_color_string(
                        drawille.unichr(drawille.braille_char_offset + char),
                        color
                    )
                    row.append(color_string)
                i += 1
            ret.append(''.join(row))

        return ret

def get_frame(filepath, resize=True, color=True):
    im = Image.open(filepath)

    if resize:
        im = resize_to_fit(im)    

    c = ImgCanvas(im)
    px = c.px 
    
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            r, g, b = get_rgb(px[x, y])
    
            if (r != 0 and r != 255) or \
               (g != 0 and g != 255) or \
               (b != 0 and b != 255):
                c.set(x, y, (r, g, b))

    return c.frame()


def display(filepath, resize=True, color=True):
    print(get_frame(filepath, resize, color))



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Path required')
        sys.exit(1)

    path = sys.argv[1]

    display(path)

