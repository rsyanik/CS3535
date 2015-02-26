#! /usr/bin/env/python

#Takes as input a local mp3 and displays two graphs.
#The graph comparing the all of the beats in the song based on
#	1. Timbre
#	2. Pitch
#Author: Reid Yanik

import echonest.remix.audio as audio
import matplotlib.pyplot as plt
import math

usage = """
Usage:
	python similarity.py <input_filename>

Example:
	python similarity.py Take_Me_to_Church.mp3
"""

def main(input_filename):
    audiofile = audio.LocalAudioFile(input_filename)
    pitches = audiofile.analysis.segments.pitches
    timbre = audiofile.analysis.segments.timbre

    pitches_sim = [[0 for x in range(len(pitches))] for x in range(len(pitches))]
    timbre_sim = [[0 for x in range(len(timbre))] for x in range(len(timbre))]

    for i in range(len(pitches)):
	for j in range(len(pitches[i])):
	     pitches_sim[i][j] = compare(pitches[i],pitches[j])
    for i in range(len(timbre)):
	for j in range(len(timbre[i])):
	     timbre_sim[i][j] = compare(timbre[i],timbre[j])

    plt.imshow(pitches_sim)
    plt.show()
    plt.imshow(timbre_sim)
    plt.show()

def compare(matrix1,matrix2):
    sum = 0
    for i in range(len(matrix1)):
        sum += ((matrix1[i] - matrix2[i])**2)
    return math.sqrt(sum)
    
if __name__ == '__main__':
    import sys
    try:
	input_filename = sys.argv[1]
    except:
        print usage
	sys.exit(-1)
    main(input_filename)        
