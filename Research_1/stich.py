#!/usr/bin/env python
# encoding: utf=8
"""
stich.py

Takes a list of songs and an output_filename to stitches rangdom sections within a random
songs in the list together to form a new song stored in outputfilename.

By Reid Yanik, 2015-03-03.
"""
import echonest.remix.audio as audio
from random import randint

def main(list,output_filename):
	list_of_sections = []
	audiofile_list = []
	for i in range(len(list)):
		audiofile = audio.LocalAudioFile(list[i])
		audiofile_list.append(audiofile)
		list_of_sections.append(audiofile.analysis.sections)
	collect = audio.AudioQuantumList()
	length = len(list_of_sections[0]
	for i in range(length):
		if i == 0
			collect.append(list_of_sections[randint(0,len(list))][0])
		elif i < length - 1
			collect.append(list_of_sections[randint(0,len(list))][randint(0,len(
