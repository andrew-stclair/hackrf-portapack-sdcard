"""Make the map database"""

from __future__ import print_function
# import sys
import struct
from PIL import Image

with open('sdcard/ADSB/world_map.bin', 'wb') as outfile:
    # Allow for bigger images
    Image.MAX_IMAGE_PIXELS = None
    im = Image.open("sdcard/ADSB/world_map.png")
    pix = im.load()
    # Write as unsigned short (2 bytes) as little endian
    outfile.write(struct.pack('<H', im.size[0]))
    outfile.write(struct.pack('<H', im.size[1]))
    print("image \t size[0]=" + str(im.size[0]) +
        "\tsize[1]=" + str(im.size[1]) + " pixels")
    print("Generating: \t" + outfile.name +
        "\n from\t\t" + im.filename + "\n please wait...")

    for y in range(0, im.size[1]):
        LINE = b''
        for x in range(0, im.size[0]):
            # RRRRRGGGGGGBBBBB
            pixel_lcd = (pix[x, y][0] >> 3) << 11
            pixel_lcd |= (pix[x, y][1] >> 2) << 5
            pixel_lcd |= (pix[x, y][2] >> 3)
            #         RRRGGGBB to
            # RRR00GGG000BB000
            # pixel_lcd = (pix[x, y][0] >> 5) << 5
            # pixel_lcd |= (pix[x, y][1] >> 5) << 2
            # pixel_lcd |= (pix[x, y][2] >> 6)
            LINE += struct.pack('<H', pixel_lcd)
        outfile.write(LINE)
        print(str(y) + '/' + str(im.size[1]), end="\r")

print("\nDone")
