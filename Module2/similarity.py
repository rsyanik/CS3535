#!/usr/bin/env python
# encoding: utf=8
"""
Similarity.py

Takes as input a local mp3 and displays two graphs.
The graph comparing the all of the beats in the song based on
	1. Timbre
	2. Pitch
"""
import echonest.remix.audio as audio
import matplotlib.image as mpimg
import numpy as np

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
    pitches_sim = [[0 for x in range(pitches.len())] for x in range(timbre.len())]
    timbre_sim = [[0 for x in range(timbre.len())] for x in range(timbre.len())]
    for i in range(pitches.len()):
	for j in range(pitches[i].len()):
	     pitches_sim[i][j] = compare(pitches[i],pitches[j])
    for i in range(timbre.len()):
	for j in range(timbre[i].len()):
	     timbre_sim[i][j] = compare(timber[i],timber[j])
    figure(1)
    imshow(pitches_sim)
    imshow(timbre_sim)
    
if __name__ == 'main':
    import sys
    try:
	input_filename = sys.argv[1]
    except:
        print usage
	sys.exit(-1)
    main(input_filename)

def compare(matrix1,matrix2):
    for i in range(matrix1):
	sum += (matrix1[i] - matrix2[i])^2
    return sqrt(sum)
        
