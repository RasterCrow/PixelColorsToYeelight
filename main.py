'''

RESIZE TUTTO LO SCHERMO IN 150x150

'''

from __future__ import print_function
import binascii
from PIL import ImageGrab
import numpy as np
import scipy.cluster
import numpy as np
import time
from yeelight import Bulb


# print(discover_bulbs())

bulb1 = Bulb("192.168.1.2")
bulb2 = Bulb("192.168.1.3")

while True:
    # This code must be run every some seconds, like 2
    NUM_CLUSTERS = 5

    # print('reading image')
    im = ImageGrab.grab()
    im = im.resize((150, 150))      # optional, to reduce time
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
    colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
    # print('most frequent is %s (#%s)' % (peak, colour))
    print(peak)
    luma = 0.2126*int(peak[0]) + 0.7152*int(peak[1]) + 0.0722*int(peak[2])
    if luma < 40:
        print('troppo scuro')
        bulb1.set_rgb(158, 0, 255)
    else:
        print(bulb1.set_rgb(int(peak[0]), int(peak[1]), int(peak[2])))

    time.sleep(1)
