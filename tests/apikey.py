import unittest
from musixmatch import *

class TestArtist(unittest.TestCase):
    def test_Artist(self):
        a1 = artist.Artist(artist_id=378462)
        a2 = artist.Artist(artist_mbid='650e7db6-b795-4eb5-a702-5ea2fc46c848')
        self.assertEqual(a1,a2)

class TestArtistsCollection(unittest.TestCase):
    def test_fromChart(self):
        c = artist.ArtistsCollection.fromChart(page=1, page_size=10)
        self.assertEqual(len(c), 10)
        for i in c:
            self.assertEqual(type(i), artist.Artist)

    def test_fromSearch(self):
        c = artist.ArtistsCollection.fromSearch(
            q='madonna', page=1, page_size=10)
        self.assertEqual(len(c), 10)
        for i in c:
            self.assertEqual(type(i), artist.Artist)

class TestTrack(unittest.TestCase):
    def test_Track(self):
        t1 = track.Track(track_id=7176425)
        t2 = track.Track(track_mbid='a5424f77-42d9-428c-9c6f-3f06ff19d756')
        self.assertEqual(t1,t2)

    def test_fromMatcher(self):
        t = track.Track.fromMatcher(
            q_track='lose yourself (album version)', q_artist='eminem')
        self.assertEqual(bool(t), True)

    def test_get(self):
        t = track.Track(track_id=6593495)
        l = t['lyrics']
        self.assertEqual(bool(l), True)
        self.assertEqual(type(l), lyrics.Lyrics)
        s = t.get('subtitle')
        self.assertEqual(bool(s), True)
        self.assertEqual(type(s), subtitle.Subtitle)
        

class TestTracksCollection(unittest.TestCase):
    def test_fromChart(self):
        c = track.TracksCollection.fromChart(page=1, page_size=10)
        self.assertEqual(len(c), 10)
        for i in c:
            self.assertEqual(type(i), track.Track)

    def test_fromSearch(self):
        c = track.TracksCollection.fromSearch(q_track='Cotton eye Joe')
        self.assertEqual(len(c), 10)
        for i in c:
            self.assertEqual(type(i), track.Track)

class TestLyrics(unittest.TestCase):
    def test_Lyrics(self):
        l = lyrics.Lyrics(track_id='4559887')
        self.assertEqual(bool(l), True)

class TestSubtitle(unittest.TestCase):
    def test_Subtitle(self):
        s = subtitle.Subtitle(track_id='6593495')
        self.assertEqual(bool(s), True)

