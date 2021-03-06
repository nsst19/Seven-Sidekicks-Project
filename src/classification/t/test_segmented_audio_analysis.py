import os
import sys
import csv

import utilities.get_song_id as s_id

from multiprocessing import Pool

from classification.segmented_audio_analysis import \
    process_data_and_extract_profiles
from similarity.split_song import split_song
from utilities.filehandler.audio_loader import get_mono_loaded_song

from pprint import pprint


def test_profile_song_data():
    filename = ("classification/t/test_segmented_audio_analysis/" +
                "8376-1-1_Demolition_Man_proud_music_preview.wav")

    split_song_list = load_and_split_song(filename)

    (segment_id, bpm,
     timbre, _, _, _,
     _, _) = process_data_and_extract_profiles(
            0,
            split_song_list[0])

    (segment_id1, bpm1,
     timbre1, _, _, _,
     _, _) = process_data_and_extract_profiles(
            1,
            split_song_list[1])

    assert segment_id == 0
    assert segment_id1 == 1
    assert bpm == (140.67031860351562, 0.0)
    assert bpm1 != (140.67031860351562, 0.0)
    assert timbre == ('dark', 0.862666606903)
    assert timbre1 != ('dark', 0.862666606903)


def test_audio_analysis_makes_csvfile():
    dirname = os.path.abspath(os.path.dirname(__file__))
    output_folder_path = os.path.join(dirname, "")
    filename = os.path.join(
        dirname,
        "test_segmented_audio_analysis/" +
        "8376-1-1_Demolition_Man_proud_music_preview.wav")
    argument_tuples = []

    song_id = s_id.get_song_id(filename)

    split_song_list = load_and_split_song(filename)

    for i in range(len(split_song_list)):
        argument_tuples.append((
            i,
            split_song_list[i]))

    csv_output_file = "{}{}_segmented_output.csv".format(
            output_folder_path, song_id)

    # CSV file header
    with open(csv_output_file, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Segment ID', 'BPM', 'Timbre',
                         'Mood Relaxed', 'Mood Party',
                         'Mood Aggressive', 'Mood Happy', 'Mood Sad'])

    csv_file.close()

    # Multithreaded runthrough of all files
    pool = Pool(8)
    res = pool.starmap(process_data_and_extract_profiles, argument_tuples)
    pool.close()

    pprint(res)

    with open(csv_output_file, 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(res)

    csv_file.close()

    assert csv_file


def load_and_split_song(filename):
    loaded_song = get_mono_loaded_song(filename)

    return split_song(loaded_song)
