from musixmatch import *
from tests import base

class TestArtist(base.TestItem):
    Class = artist.Artist
    item = {
        "artist_id": "292",
        "artist_mbid": "292",
    }
    item_str = "{   'artist_id': '292',\n    'artist_mbid': '292'}"
    item_repr = "Artist({'artist_mbid': '292', 'artist_id': '292'})"
    item_hash = 292

class TestArtistsCollection(base.TestCollection):
    CollectionClass = artist.ArtistsCollection
    AllowedContentClass = artist.ArtistsCollection.allowedin()
    item_list = 'artist_list'
    item_id = 'artist_id'
    item = 'artist'
    message = {
        "body": {
            "artist_list": [
                {
                    "artist": {
                        "artist_id": "292",
                        "artist_mbid": "292",
                    }
                },
                {
                    "artist": {
                        "artist_id": "8976",
                        "artist_mbid": "8976",
                    }
                },
                {
                    "artist": {
                        "artist_id": "9673",
                        "artist_mbid": "9673",
                    }
                }
            ]
        },
        "header": {
            "execute_time": 0.14144802093506001,
            "status_code": 200
        }
    }

