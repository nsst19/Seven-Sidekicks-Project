import os

from classification.classifier.profile_data_extractor \
    import get_classifier_data


def test_profile_song_data():
    # This is the setup required to dynamically run this
    # test from anywhere you'd like.
    dirname = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(
        dirname,
        "test_classifier/8376-1-1_output.json")

    song_data = get_classifier_data(filename)

    assert song_data is not None
    assert song_data[0] == ("dark", 0.728462159634)
    assert song_data[1] == ("not_relaxed", 0.980210959911)
    assert song_data[2] == ("not_party", 0.643296301365)
    assert song_data[3] == ("aggressive", 0.993713259697)
    assert song_data[4] == ("not_happy", 0.926596462727)
    assert song_data[5] == ("not_sad", 0.977098941803)
