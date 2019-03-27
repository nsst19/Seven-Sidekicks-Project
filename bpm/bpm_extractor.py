import sys
import os

import utilities.get_song_id as s_id
# End of importing the utilities module

from multiprocessing import Pool
from tabulate import tabulate

from essentia.standard import RhythmExtractor2013

def get_song_bpm(audio):
    rhythm_extractor = RhythmExtractor2013()
    bpm, _, beats_confidence, _, _ = rhythm_extractor(audio)

    return bpm, beats_confidence


if __name__ == "__main__":
    files = []
    for file in os.listdir(sys.argv[1]):
        if file.endswith(".wav"):
            files.append(os.path.join(sys.argv[1], file))

    pool = Pool(8)
    res = pool.map(get_song_bpm, files)
    pool.close()

    print(tabulate(res,
                   headers=[ 'BPM', 'Confidence'],
                   tablefmt='orgtbl'))
