import datetime
import typing


from pymongo import MongoClient
from utilities.config_loader import load_config


def _create_default_document(id: int) -> Dict:
    """Gives a database entity an id and a timestamp
    
    Parameters
    ----------
    id
        id of the entity to be created
        
    Returns
    -------
    Dict
        containing id and timestamp
    """

    return {
        "segment_id": id,
        "last_updated": datetime.datetime.utcnow(),
    }
 
def _augment_document(doc1: dict, doc2: dict) -> Dict:
    """Combines parameters into a larger dictionary
    
    Parameters
    ----------
    doc1
        first dictionary
    doc2
        second dictionary
        
    Returns
    -------
    Dict
        dictionary combining two dictionaries
    """


# Generic class for making functions implementable
# for lower level classes of music analysis
class Database:
    """
    A database class used to communicate with a database

    Methods
    -------
    def insert(self, col, song_id: int, doc: dict) -> int
        inserts data into the collection in the database

    def find(self, col, song_id: int):
        finds one entity given an id

    def find_all_by_id(self, name, song_id: int):
        finds all entities given an id

    def find_all(self, col):
        finds all entities in the database

    def close(self):
        closes the database
    
    """

    def __init__(self):
        cfg = load_config()

        self._client = MongoClient(
            cfg['mongo_host'], cfg['mongo_port'],
            username=cfg['mongo_user'],
            password=cfg['mongo_pass'])
        self._db = self._client[cfg['mongo_db']]

    def insert(self, col, song_id: int, doc: dict) -> int:
        """Insert data into the collection
    
        Parameters
        ----------
        self
            the entity itself
        col
            the collection to be added to
        song_id
            id of the song
        doc
            dictionary with data
            
        Returns
        -------
        int
            an int of the id
        """

        collection = self._db[col]
        ins = _augment_document(_create_default_document(song_id), doc)
        _id = collection.insert_one(ins).inserted_id
        return _id

# Gets the newest entry, the other option would be to overwrite it in the insert method
    def find(self, col, song_id: int):
        """Find one instance of the data requested
    
        Parameters
        ----------
        self
            the entity itself
        col
            the collection to be added to
        song_id
            id of the song
            
        Returns
        -------
        Object
            either a None Object or the Object from the database
        """
        if (self._db[col].count({'song_id': song_id}) > 0):
            res = self._db[col].find({'song_id': song_id}
                                      ).sort([('last_updated', -1)]
                                             ).limit(1)
            return res[0]

        return None

    def find_all_by_id(self, name, song_id: int):
        """Find all instances of the data requested in the collection by song_id
    
        Parameters
        ----------
        self
            the entity itself
        col
            the collection to be added to
        song_id
            id of the song
            
        Returns
        -------
        Object list
            a list of the Objects in the database from a given song_id
        """

        results = []
        for res in self._db[name].find({'song_id': song_id}):
            results.append(res)
        return results

    def find_all(self, col):
        """Find all instances of the data requested in the collection
    
        Parameters
        ----------
        self
            the entity itself
        col
            the collection to be added to
            
        Returns
        -------
        Object list
            a list of the Objects in the database
        """

        results = []
        for r in self._db[col].find():
            results.append(r)
        return results

    def close(self):
        """closes the connection to the database"""
        self._client.close()
