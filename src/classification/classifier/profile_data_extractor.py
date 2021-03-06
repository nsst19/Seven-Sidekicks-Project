import os
import subprocess
import json
from typing import Tuple

from tempfile import NamedTemporaryFile

from utilities.filehandler.handle_path import get_absolute_path


def get_classifier_data(
    data_file_name: str) -> Tuple[
        Tuple, Tuple, Tuple, Tuple, Tuple, Tuple]:
    """Extracts the highlevel mood classifications from a given song file

    Parameters
    ----------
    data_file_name
        single song file path

    Returns
    -------
    Tuple[Tuple, Tuple, Tuple, Tuple, Tuple, Tuple]
        A tuple of tuples describing all moods and their probability
    """

    # This setup is required, to dynamically run this
    # test from anywhere you'd like.
    dirname = os.path.abspath(os.path.dirname(__file__))
    profile_file = get_absolute_path("utilities/ressources/" +
                                     "timbre_moods_profile.yaml")

    # Temp file used instead of writing to an actual file
    temp_file = NamedTemporaryFile(delete=True)

    command = 'essentia_streaming_extractor_music_svm {} {} {}'.format(
        data_file_name, temp_file.name, profile_file)

    subprocess.run("cd {} && {}".format(dirname, command), shell=True)

    data = json.load(temp_file)

    temp_file.close()

    # Setting the data JSON data up in variables
    highlevel = data['highlevel']

    timbre = highlevel['timbre']['value']
    timbre_probability = highlevel['timbre']['probability']

    mood_relaxed = highlevel['mood_relaxed']['value']
    mood_relaxed_probability = highlevel['mood_relaxed']['probability']

    mood_party = highlevel['mood_party']['value']
    mood_party_probability = highlevel['mood_party']['probability']

    mood_aggressive = highlevel['mood_aggressive']['value']
    mood_aggressive_probability = highlevel['mood_aggressive']['probability']

    mood_happy = highlevel['mood_happy']['value']
    mood_happy_probability = highlevel['mood_happy']['probability']

    mood_sad = highlevel['mood_sad']['value']
    mood_sad_probability = highlevel['mood_sad']['probability']

    # list for beautifying code
    t = [(timbre, timbre_probability),
         (mood_relaxed, mood_relaxed_probability),
         (mood_party, mood_party_probability),
         (mood_aggressive, mood_aggressive_probability),
         (mood_happy, mood_happy_probability),
         (mood_sad, mood_sad_probability)
         ]

    return t[0], t[1], t[2], t[3], t[4], t[5]
