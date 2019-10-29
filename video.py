import imageio
from termglyph import *

vid = imageio.get_reader("assets/video-1535271957.mp4", "ffmpeg")

for im in vid:
    c = ImgCanvas(im)
    px = c.px 
    
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            r, g, b = get_rgb(px[x, y])
    
            if (r != 0 and r != 255) or \
               (g != 0 and g != 255) or \
               (b != 0 and b != 255):
                c.set(x, y, (r, g, b))

    print(c.frame())

