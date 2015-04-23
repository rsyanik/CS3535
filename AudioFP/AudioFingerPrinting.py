#! /usr/bin/env/python

import matplotlib.pyplot as plt
from matplotlib import mlab
import numpy as np
import scipy as sp
import scipy.io.wavfile as wav

def main(inputFile):
    (fs,stereo) = wav.read(inputFile)
    mono = stereoToMono(stereo)
    mono = np.array(mono)
    Pxx, freqs, bins, im = plt.specgram(mono,Fs = fs)
    plt.show()

def stereoToMono(stereo):
    return [(stereo[:,0] + stereo[:,1]) / 2]


if __name__ == '__main__':
    import sys
    try:
        inputFile = sys.argv[1]
    except:
        print "Need input file"
        sys.exit(-1)
    main(inputFile)
