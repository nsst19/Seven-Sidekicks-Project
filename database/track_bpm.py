from database.database import Database
from database.storinator import Storinator


class TrackBPM(Storinator):
    def __init__(self, host="localhost", port=27017,
                 username=None, password=None):
        self._dbname = 'track_bpm'
        self._db = Database(host, port, username, password)

    def add(self, song_id, bpm, confidence):
        return self._db.insert(self._dbname, song_id, {
            "bpm": bpm,
            "confidence": confidence
        })

    def get(self, song_id):
        return self._db.find(self._dbname, song_id)

    def get_all(self):
        return self._db.find_all(self._dbname)

    def close(self):
        self._db.close()
