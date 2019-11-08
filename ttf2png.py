import sys
import click
import subprocess
import os


@click.command()
@click.option('--font', '-f', help='Path to font file', required=True)
@click.option('--start', '-s', default='a', help='Glyph to start with')
@click.option('--end', '-e', default='z', help='Glyph to end with')
@click.option('--out', '-o', default='out', help='Output directory name')
def main(font, start, end, out):
    subprocess.call(['mkdir', out]) 

    for i in range(ord(start), ord(end) + 1):
        glyph = chr(i)
        command = 'convert -background none -fill black -font {} -pointsize 300 label:"{}" {}' .format(font, glyph, os.path.join(out, glyph + '.png'))
        os.system(command)

if __name__ == '__main__':
    main()
 
