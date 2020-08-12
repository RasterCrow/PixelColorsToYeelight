
'''

senza media tra i due colori

'''

from __future__ import print_function
import binascii
from PIL import ImageGrab
import numpy as np
import scipy.cluster
import numpy as np
import time
from yeelight import Bulb
from win32api import GetSystemMetrics
import pyautogui

# print(discover_bulbs())

bulb1 = Bulb("192.168.1.2")
bulb2 = Bulb("192.168.1.3")
NUM_CLUSTERS = 5
difference = 200
while True:

    x, y = pyautogui.position()
    # This code must be run every some seconds, like 2
    # print('reading image')

    screen_width = GetSystemMetrics(0)
    screen_height = GetSystemMetrics(1)

    # h, w = image.shape[:-1]  # height and width of searched image

    x1 = min(int(x-difference), screen_width)
    y1 = min(int(y-difference), screen_height)
    x2 = min(int(x+difference), screen_width)
    y2 = min(int(y+difference), screen_height)

    search_area = (x1, y1, x2, y2)

    im = ImageGrab.grab().crop(search_area)

    ar = np.asarray(im)
    shape = ar.shape
    ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)

    # print('finding clusters')
    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
    # print('cluster centres:\n', codes)

    vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
    counts, bins = np.histogram(vecs, len(codes))    # count occurrences

    index_max = np.argmax(counts)                    # find most frequent
    peak = codes[index_max]
    # print('most frequent is %s (#%s)' % (peak, colour))
    print(peak)

    luma = 0.2126*int(peak[0]) + 0.7152*int(peak[1]) + 0.0722*int(peak[2])
    if luma < 30:
        print('troppo scuro')
        bulb1.set_rgb(158, 0, 255)
        bulb2.set_rgb(158, 0, 255)
    elif luma > 130:
        print(bulb1.set_color_temp(6000))
        print(bulb2.set_color_temp(6000))
    else:
        print(bulb1.set_rgb(int(peak[0]), int(peak[1]), int(peak[2])))
        print(bulb2.set_rgb(int(peak[0]), int(peak[1]), int(peak[2])))

    time.sleep(1)
