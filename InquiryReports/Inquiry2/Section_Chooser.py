#!/usr/bin/env python
# encoding: utf=8
"""
section_chooser.py

given a mp3 file and a section number, digests that sections and outputs only that sections.

By Reid Yanik, 2015-03-03
"""
import echonest.remix.audio as audio

usage = """
Usage:
	python section_chooser.py <input_filename> <integer number> <output_filename?

Example:
	python section_chooser.py "Centuries.mp3" 3 "Fourth_Section Centuries.mp3"
"""

def main(input_filename, section_number, output_filename):
	audiofile = audio.LocalAudioFile(input_filename)
	sections = audiofile.analysis.sections
	collect = audio.AudioQuantumList()
	collect.append(sections[section_number])
	out = audio.getpieces(audiofile, collect)
	out.encode(output_filename)

if __name__ == '__main__':
	import sys
	try:
		input_filename = sys.argv[1]
		section_number = int(sys.argv[2])
		output_filename = sys.argv[3]
	except:
		print usage
		sys.exit(-1)
	main(input_filename, section_number, output_filename)
