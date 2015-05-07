#!/usr/bin/env python

import echonest.remix.audio as audio
import os
import pickle
import sys
import shutil
import hashlib
import math
import random
from collections import defaultdict

AUDIO_EXTENSIONS = {'mp3', 'm4a', 'wav', 'ogg', 'au', 'mp4'}
PLAYLIST_DIR = 'playlist'

def _is_audio(f_):
    _, ext = os.path.splitext(f_)
    # drop leading '.'
    ext = ext[1:]
    return ext in AUDIO_EXTENSIONS

def _is_playlist(f_):
    from re import search
    return search(r".*\.play\.pkl", f_) is not None


def _is_md5(x_):
    from re import match
    return match('[a-z0-9]{32}', x_) is not None


def get_md5(song_file_):
    return hashlib.md5(file(song_file_, 'rb').read()).hexdigest()

def all_used(used):
    for md5_ in used:
        if used[md5_] == False:
            return False
    return True

def clear_md5(used):
    for md5_ in used:
        used[md5_] = False

def check_keys(local_audio,beats):
    return local_audio.keys() == beats.keys()

def get_all_songs(directory_):
    all_songs_ = []
    for f_ in os.listdir(directory_):
        path_ = os.path.join(directory_, f_)
        if os.path.isdir(path_):
            all_songs_.extend(get_all_songs(path_))
        elif _is_audio(path_):
            all_songs_.append(path_)

    return all_songs_

def get_beats(local_audio_):
    beats = defaultdict(dict)
    for md5_ in local_audio_.keys():
        laf_ = local_audio_[md5_]
        beats[md5_] = laf_.analysis.beats
    print beats.keys()
    return beats


def robust_local_audio_file(audio_file):
    from time import sleep
    from pyechonest.util import EchoNestAPIError
    try:
        laf_ = audio.LocalAudioFile(audio_file)
        return laf_
    except EchoNestAPIError:
        print "Failed to retrieve analysis... wait to try again"
        sleep(10)
        return robust_local_audio_file(audio_file)

def get_local_audio(all_songs_):
    from shutil import copyfile
    local_audio_ = {}
    for i_ in range(len(all_songs_)):
        print 'get song', (i_ + 1), '/', len(all_songs_)
        print 'Title:', all_songs_[i_]
        extension = os.path.splitext(all_songs_[i_])[1]
        track_md5_ = get_md5(all_songs_[i_])
        mp3_file = PLAYLIST_DIR + "/" + track_md5_ + extension
        if not os.path.isfile(mp3_file):
            print "copying original audio to", mp3_file
            if not os.path.exists(PLAYLIST_DIR):
                os.makedirs(PLAYLIST_DIR)
            copyfile(all_songs_[i_], mp3_file)

        print "loading local audio from", mp3_file
        laf_ = robust_local_audio_file(mp3_file)
        local_audio_[track_md5_] = laf_
    return local_audio_

def distance(beat1, beat2):
    if len(beat1.segments) > len(beat2.segments):
        segs = len(beat2.segments)
    else:
        segs = len(beat1.segments)
    total = 0
    for seg in range(0, segs):
        total += get_seg_distances(beat1.segments[seg], beat2.segments[seg])
    average = total / segs
    return average

def get_seg_distances(segments_1, segments_2):
    timbreWeight = 1
    pitchWeight = 10
    loudStartWeight = 1
    loudMaxWeight = 1
    durationWeight = 100
    confidenceWeight = 1

    timbre = seg_distance(segments_1, segments_2, 'timbre')
    pitch = seg_distance(segments_1, segments_2, 'pitches')

    sloudStart = math.fabs(segments_1.loudness_begin - segments_2.loudness_begin)
    sloudMax = math.fabs(segments_1.loudness_max - segments_2.loudness_max)
    duration = math.fabs(segments_1.duration - segments_2.duration)
    if segments_1.confidence != None and segments_2.confidence != None:
        confidence = math.fabs(segments_1.confidence - segments_2.confidence)
    else:
        confidence = 0
    distance = (timbre * timbreWeight) + (pitch * pitchWeight) + (sloudStart * loudStartWeight) + \
               (sloudMax * loudMaxWeight) + (duration * durationWeight) + (confidence * confidenceWeight)
    return distance

def seg_distance(segment_1, segment_2, type):
    if type == 'timbre':
        return euclidean_distance(segment_1.timbre, segment_2.timbre)
    return euclidean_distance(segment_1.pitches, segment_2.pitches)

def euclidean_distance(v1,v2):
    sum = 0
    for i in range(0, len(v1)):
        delta = v2[i] - v1[i]
        sum += delta * delta
    return math.sqrt(sum)

def get_closest_beat(beats, target_beat,MD5):
    min = distance(target_beat,beats[random.choice(list(beats.keys()))][0])
    min_md5_ = MD5
    min_beat_index = 0
    for md5_ in beats:
        for i in range(len(beats[md5_])):
            if(md5_ != MD5):
                temp_dist = distance(target_beat,beats[md5_][i])
                if(temp_dist < min and temp_dist > 0):
                    min = temp_dist
                    min_md5_ = md5_
                    min_beat_index = i
    print "Final min:",min
    return(min_md5_, min_beat_index)

def my_get_pieces(local_audio, beats):
    print "keys are the same: ", check_keys(local_audio,beats)
    MD5 = random.choice(list(local_audio.keys()))
    laf_ = local_audio[MD5]
    md5_list = {}
    used = {}

    for md5_ in local_audio:
        used[md5_] = False

    dur = 0
    channels = laf_.data.shape[1]
    newSampleRate = laf_.sampleRate
    newVerbose = laf_.verbose

    NUM_OF_SECTIONS = 3 * len(laf_.analysis.sections)
    NUM_BPS = 25           # Number of beats per song
    section_index = 0       # section number of the song we are creating
    section_num = 0         # section number of the song we are choosing from
    beat_index = 0          # beat index of the section that we start from
                            # between (0 - len(bars[section_num].children()))

    temp_beats = defaultdict(dict)
    while(section_index < NUM_OF_SECTIONS):
        print "Section ", (section_index + 1), " of ", NUM_OF_SECTIONS
        print "MD5: ", MD5
        collect = audio.AudioQuantumList()
        temp_num_BPS = NUM_BPS
        md5_list[section_index] = MD5

        # collecting the NUM_BPS beats in a song
        temp_beats[section_index] = audio.AudioQuantumList()
        if(beat_index + (NUM_BPS - 1) > len(beats[MD5])):
            temp_num_BPS = len(beats[MD5]) - (beat_index + 1)
        for i in range(temp_num_BPS):
            temp_beats[section_index].append(beats[MD5][beat_index + i])
        md5_list[section_index] = MD5
        section_index = section_index + 1
        (MD5,beat_index) = get_closest_beat(beats,beats[MD5][beat_index + (temp_num_BPS - 1)], MD5)

    for i in range(len(temp_beats)):
        for j in range(len(temp_beats[i])):
            dur += int(newSampleRate * temp_beats[i][j].duration)
    print "duration: ",dur
    newShape = (dur,channels)

    newAD = audio.AudioData(shape=newShape, sampleRate=newSampleRate,
                        numChannels=channels, defer=False,verbose=newVerbose)

    for i in range(len(temp_beats)):
        new_md5 = md5_list[i]
        new_laf_ = local_audio[new_md5]
        for j in range(len(temp_beats[i])):
            newAD.append(new_laf_[temp_beats[i][j]])

    return newAD

def main(playlist, output_filename):
    # Set up
    all_songs = get_all_songs(playlist)
    for i in range(len(all_songs)):
        print "song ",i,": ",all_songs[i]
    local_audio = get_local_audio(all_songs)
    beats = get_beats(local_audio)

    out = my_get_pieces(local_audio,beats)
    out.encode(output_filename)

if __name__ == '__main__':
    import sys
    try:
        if os.path.isdir(sys.argv[1]):
            playlist = sys.argv[1]
        else:
            print "Need directory for playlist as first command line argument."
            sys.exit(-1)
        output_filename = sys.argv[2]
    except:
        print usage
        sys.exit(-1)
    main(playlist,output_filename)
