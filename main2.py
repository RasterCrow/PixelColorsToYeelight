
'''

CON GET PIXEL IN MEZZO

'''

from PIL import Image
from PIL import ImageGrab
import time
from yeelight import Bulb


# print(discover_bulbs())

bulb1 = Bulb("192.168.1.2")
bulb2 = Bulb("192.168.1.3")

while True:
    # This code must be run every some seconds, like 2
    # print('reading image')
    im = ImageGrab.grab()
    #img2 = im.resize((1, 1))
    #img2 = im.resize((1, 1))
    color = im.getpixel((0, 0))
    print(color)
    luma = 0.2126*int(color[0]) + 0.7152*int(color[1]) + 0.0722*int(color[2])
    if luma < 30:
        print('troppo scuro')
        bulb1.set_rgb(158, 0, 255)
    else:
        print(bulb1.set_rgb(int(color[0]), int(color[1]), int(color[2])))

    time.sleep(1.1)
