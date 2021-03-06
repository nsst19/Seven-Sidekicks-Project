from bpm.bpm_extractor import get_song_bpm
from utilities.filehandler.audio_loader import get_mono_loaded_song


def test_get_song_bpm():
    song = get_mono_loaded_song("bpm/t/test_bpm_extractor/8376-1-" +
                                "1_Demolition_Man_proud_music_preview.wav")
    bpm, confidence = get_song_bpm(song)

    assert round(bpm, 3) == 139.847
    assert round(confidence, 4) == 2.4134
