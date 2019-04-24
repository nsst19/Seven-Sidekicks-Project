import datetime

from pymongo import MongoClient

from utilities.config_loader import load_config


def _create_default_document(id, id2):
    return {
        "song_id": id,
        "video_id": id2,
        "last_updated": datetime.datetime.utcnow(),
    }


def _augment_document(vme_id, bpm, timbre,
                      party, relaxed, emotions):
    return {**vme_id, **bpm, **timbre, **party, **relaxed, **emotions}


class VMEDatabase:
    def __init__(self):
        cfg = load_config()

        self._client = MongoClient(
            cfg['mongo_host'], cfg['mongo_port'],
            username=cfg['mongo_user'], password=cfg['mongo_pass'])
        self._db = self._client['dr']

    def insert(self, name, song_id, video_id,
               bpm, timbre, party, relaxed, emotions):
        collection = self._db[name]
        ins = _augment_document(_create_default_document(song_id, video_id),
                                bpm, timbre, party, relaxed, emotions)
        id = collection.insert_one(ins).inserted_id
        return id

    def find(self, name,
             song_id, video_id):
        return self._db[name].find({'song_id': song_id, 'video_id': video_id}
                                   ).sort([('last_updated', -1)]
                                          ).limit(1)[0]

    def find_all(self, name):
        results = []
        for track_bpm in self._db[name].find():
            results.append(track_bpm)
        return results
