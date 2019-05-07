import datetime


from typing import Dict


from pymongo import MongoClient
from utilities.config_loader import load_config


def _create_default_document(id: int, id2: int) -> Dict:
    """Gives a database entity an id and a timestamp
    
    Parameters
    ----------
    id1
        song_id of the entity to be created
    id2
        video_id of the entity to be created
        
    Returns
    -------
    Dict
        Containing id and timestamp
    """

    return {
        "song_id": id,
        "video_id": id2,
        "last_updated": datetime.datetime.utcnow(),
    }

def _augment_document(id1: dict, time: dict, emotion: dict) -> Dict:
    """Combines parameters into a larger dictionary
    
    Parameters
    ----------
    id1
        id of the entity
    time
        dictionary of time interval
    emotion
        dictionary of emotion data
        
    Returns
    -------
    Dict
        Dictionary combining id, time interval and emotion data
    """

    return {**id1, **time, **emotion}


# Generic class for making functions implementable
# for lower level classes of music analysis
class VEDatabase:
    """
    A database class used to communicate with a database

    Methods
    -------
    def __init__(self)
        Creates the individual collection in the database
        
    def insert(self, col,
               song_id: int, video_id: int, 
               time: dict, emotion: dict) -> int:
        Inserts data into the collection in the database

    def find(self, col,
             song_id: int, video_id: int):
        Finds one entity given an id

    def find_by_song_id(self, col, song_id: int):
        Finds all entities given an id

    def find_all(self, col):
        Finds all entities in the database

    def close(self):
        Closes the database
    
    """

    def __init__(self):

        cfg = load_config()

        self._client = MongoClient(
            cfg['mongo_host'], cfg['mongo_port'],
            username=cfg['mongo_user'], password=cfg['mongo_pass'])
        self._db = self._client[cfg['mongo_db']]

    def insert(self, col,
               song_id: int, video_id: int, 
               time: dict, emotion: dict) -> int:
        """Insert data into the collection
    
        Parameters
        ----------
        col
            The collection to be added to
        song_id
            id of the song
        video_id
            id of the video
        doc
            Dictionary with data
            
        Returns
        -------
        int
            An int of the id
        """

        collection = self._db[col]

        ins = _augment_document(
            _create_default_document(song_id,video_id),
             time, emotion)
        id = collection.insert_one(ins).inserted_id
        return id

    def find(self, col,
             song_id: int, video_id: int):
        """Find one instance of the data requested
    
        Parameters
        ----------
        col
            The collection to be added to
        song_id
            id of the song
        video_id
            id of the videos
            
        Returns
        -------
        Object
            Either a None Object or the Object from the database
        """

        return self._db[col].find({'song_id': song_id, 'video_id': video_id}
                                  ).sort([('last_updated', -1)]
                                         ).limit(1)[0]

    def find_by_song_id(self, col, song_id: int):
        """Find all instances of the data requested in the collection by song_id
    
        Parameters
        ----------
        col
            The collection to be added to
        song_id
            id of the song
            
        Returns
        -------
        Object list
            A list of the Objects in the database from a given song_id
        """

        results = []
        data =  self._db[col].find({'song_id': song_id})
        for i in data:
            del i['_id']
            i['last_updated'] = i['last_updated'].isoformat()
            results.append(i)
        return results

    def find_all(self, col):
        """Find all instances of the data requested in the collection
    
        Parameters
        ----------
        col
            The collection to be added to
            
        Returns
        -------
        Object list
            A list of the Objects in the database
        """

        results = []
        for r in self._db[col].find():
            results.append(r)

        return results

    def close(self):

        self._client.close()
