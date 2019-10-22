from drawille import *
from collections import defaultdict
from PIL import Image


COLOR_CONVERSION_RATIO = 2**8 // 5


def cprint(text, color, background=False, *args, **kwargs):
    fg = lambda text, color: "\33[38;5;" + str(color) + "m" + text + "\33[0m"
    bg = lambda text, color: "\33[48;5;" + str(color) + "m" + text + "\33[0m"

    format_f = bg if background else fg

    if color >= 0:
        print(format_f(text, color), *args, **kwargs)

def get_color_string(text, color):
    format_f = lambda text, color: "\33[38;5;" + str(color) + "m" + text + "\33[0m"

    if color >= 0:
        return format_f(text, color)
    else:
        return text


def get_rgb(pix):
    return pix[0], pix[1], pix[2]


def convert_rgb_to_666(pix_color):
    # TODO: Add grayscale
    r, g, b = pix_color
    r = r // COLOR_CONVERSION_RATIO 
    g = g // COLOR_CONVERSION_RATIO
    b = b // COLOR_CONVERSION_RATIO

    return 16 + r * 36  + g * 6 + b


def start_color(color):
    print("\33[38;5;" + str(color) + "m")


def end_color():
    print("\33[0m")


set_i = 0
class ImgCanvas(Canvas):
    def __init__(self, image, *args, **kwargs):
        """
        :param image PIL loaded image (png format for now)
        """
        # TODO: Support other than png format

        super().__init__(*args, **kwargs)
        self.image = image
        self.px = image.load()

    def clear(self):
        super().clear()
        self.colors = defaultdict(intdefaultdict)

    def set(self, x, y):
        """Set a pixel of the :class:`Canvas` object.
        :param x: x coordinate of the pixel
        :param y: y coordinate of the pixel
        """
        x = normalize(x)
        y = normalize(y)
        col, row = get_pos(x, y)

        global set_i

        if type(self.chars[row][col]) != int:
            return

        self.chars[row][col] |= pixel_map[y % 4][x % 2]
        self.colors[row][col] += convert_rgb_to_666(get_rgb(self.px[x, y])) 

        print('{}: Set color: {}'
              .format(set_i, convert_rgb_to_666(get_rgb(self.px[x, y]))))

        set_i += 1
#        print ('row: {}, col: {}, x: {}, y: {}'
#               .format(row, col, x, y))


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
                    row.append(unichr(braille_char_offset))
                elif type(char) != int:
                    row.append(char)
                else:
                    print('{}: Print color: {}'.format(i, color))
                    row.append(get_color_string(unichr(braille_char_offset+char), color))
#                    row.append(unichr(braille_char_offset+char))
                i += 1
            ret.append(''.join(row))

        return ret


def main():
    im = Image.open("assets/building.png")
#    im = im.resize((400, 400))
    px = im.load()
    
    # TODO: Resize image properly
    # print(get_terminal_size())
    # 
    # term_w, term_h = get_terminal_size()
    # im_width, im_height = im.size
    # 
    # w_ratio = im_width / term_w 
    # h_ratio = im_height / term_h
    # 
    # ratio = w_ratio if w_ratio > h_ratio else h_ratio
    # if ratio > 1:
    #     new_width = int(im_width // ratio)
    #     new_height = int(im_height // ratio)
    #     im = im.resize((new_width, new_height))
    
    c = ImgCanvas(im)
    
    for x in range(im.size[1]):
        for y in range(im.size[0]):
            r, g, b = get_rgb(px[x, y])
    
            if (r != 0 and r != 255) or \
               (g != 0 and g != 255) or \
               (b != 0 and b != 255):
                c.set(x, y)

#    frame = c.frame()
    
    print(c.frame())
    a = get_color_string('WHAT', 120)
    b = get_color_string('WHAT', 220)
    c = get_color_string('WHAT', 180)

    print(a, b, c)
    print('Kanapeczki')

    

if __name__ == '__main__':
    main()

