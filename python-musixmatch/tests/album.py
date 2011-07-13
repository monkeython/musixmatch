import unittest
from musixmatch import album
from musixmatch import api
from tests import base


class TestAlbum(base.TestItem):
    Class = album.Album
    item = {
        "album_id": "292",
        "album_name": "292",
    }
    item_str = "{   'album_id': '292',\n    'album_name': '292'}"
    item_repr = "Album({'album_name': '292', 'album_id': '292'})"
    item_hash = 292

class TestAlbumsCollection(base.TestCollection):
    CollectionClass = album.AlbumsCollection
    AllowedContentClass = album.AlbumsCollection.allowedin()
    item_list = 'album_list'
    item_id = 'album_id'
    item = 'album'
    message = {
        "body": {
            "album_list": [
                {
                    "album": {
                        "album_id": "292",
                        "album_name": "292",
                    }
                },
                {
                    "album": {
                        "album_id": "8976",
                        "album_name": "8976",
                    }
                },
                {
                    "album": {
                        "album_id": "9673",
                        "album_name": "9673",
                    }
                }
            ]
        },
        "header": {
            "execute_time": 0.14144802093506001,
            "status_code": 200
        }
    }

