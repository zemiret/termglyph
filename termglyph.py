from drawille import Canvas, getTerminalSize as get_terminal_size 
from PIL import Image


COLOR_CONVERSION_RATIO = 2**8 // 5


def cprint(text, color, background=False, *args, **kwargs):
    fg = lambda text, color: "\33[38;5;" + str(color) + "m" + text + "\33[0m"
    bg = lambda text, color: "\33[48;5;" + str(color) + "m" + text + "\33[0m"

    format_f = bg if background else fg

    if color >= 0:
        print(format_f(text, color), *args, **kwargs)


def get_rgb(pix):
    return pix[0], pix[1], pix[2]


def covert_rgb_to_666(pix_color):
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


class ImgCanvas(Canvas):
    def __init__(self, *args, **kwrgs):
        super().__init__(*args, **kwargs)


def main():
    im = Image.open("assets/dab.png")
    im = im.resize((400, 400))
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
    
    c = Canvas()
    
    for x in range(im.size[1]):
        for y in range(im.size[0]):
            r, g, b = get_rgb(px[x, y])
    
            if (r != 0 and r != 255) or \
               (g != 0 and g != 255) or \
               (b != 0 and b != 255):
                c.set(x, y)
    
    # print(c.frame())
    
