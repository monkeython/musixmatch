from musixmatch import *
from tests import base

class TestLyrics(base.TestItem):
    Class = lyrics.Lyrics
    item = {
        "lyrics_id": "292",
        "lyrics_mbid": "292",
    }
    item_str = "{   'lyrics_id': '292',\n    'lyrics_mbid': '292'}"
    item_repr = "Lyrics({'lyrics_id': '292', 'lyrics_mbid': '292'})"
    item_hash = 292
