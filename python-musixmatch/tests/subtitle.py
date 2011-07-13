import unittest
from musixmatch import subtitle
from musixmatch import api
from tests import base

class TestSubtitle(base.TestItem):
    Class = subtitle.Subtitle
    item = {
        "subtitle_id": "292",
        "subtitle_mbid": "292",
    }
    item_str = "{   'subtitle_id': '292',\n    'subtitle_mbid': '292'}"
    item_repr = "Subtitle({'subtitle_mbid': '292', 'subtitle_id': '292'})"
    item_hash = 292
