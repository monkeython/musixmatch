from musixmatch import *
from tests import base

class TestTrack(base.TestItem):
    Class = track.Track
    item = {
        "track_id": "292",
        "track_mbid": "292",
    }
    item_str = "{   'track_id': '292',\n    'track_mbid': '292'}"
    item_repr = "Track({'track_mbid': '292', 'track_id': '292'})"
    item_hash = 292

class TestTracksCollection(base.TestCollection):
    CollectionClass = track.TracksCollection
    AllowedContentClass = track.TracksCollection.allowedin()
    item_list = 'track_list'
    item_id = 'track_id'
    item = 'track'
    message = {
        "body": {
            "track_list": [
                {
                    "track": {
                        "track_id": "292",
                        "track_mbid": "292",
                    }
                },
                {
                    "track": {
                        "track_id": "8976",
                        "track_mbid": "8976",
                    }
                },
                {
                    "track": {
                        "track_id": "9673",
                        "track_mbid": "9673",
                    }
                }
            ]
        },
        "header": {
            "execute_time": 0.14144802093506001,
            "status_code": 200
        }
    }

