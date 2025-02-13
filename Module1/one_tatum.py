#!/usr/bin/env python
# encoding: utf=8
"""
one.py

Digests only the first tatum in a beat 

By Reid Yanik based on one.py from Ben Lacker, 2009-02-18.
"""
import echonest.remix.audio as audio

usage = """
Usage: 
    python one_tatum.py <input_filename> <output_filename>

Example:
    python one_tatum.py EverythingIsOnTheOne.mp3 EverythingIsReallyOnTheOne.mp3
"""

def main(input_filename, output_filename):
    audiofile = audio.LocalAudioFile(input_filename)
    beats = audiofile.analysis.beats
    collect = audio.AudioQuantumList()
    for beat in beats:
        collect.append(beat.children()[0])
    out = audio.getpieces(audiofile, collect)
    out.encode(output_filename)

if __name__ == '__main__':
    import sys
    try:
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
    except:
        print usage
        sys.exit(-1)
    main(input_filename, output_filename)
