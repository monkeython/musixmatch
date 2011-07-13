import os
from unittest import defaultTestLoader, TestSuite
import api
import apikey
import artist
import base
import lyrics
import subtitle
import track
import album

suite = TestSuite()
suite.addTest(defaultTestLoader.loadTestsFromModule(api))
suite.addTest(defaultTestLoader.loadTestsFromModule(artist))
suite.addTest(defaultTestLoader.loadTestsFromModule(base))
suite.addTest(defaultTestLoader.loadTestsFromModule(lyrics))
suite.addTest(defaultTestLoader.loadTestsFromModule(subtitle))
suite.addTest(defaultTestLoader.loadTestsFromModule(track))
suite.addTest(defaultTestLoader.loadTestsFromModule(album))
if os.environ.get('musixmatch_apikey', None):
    suite.addTest(defaultTestLoader.loadTestsFromModule(apikey))

# suite.addTest(api.TestError())
# suite.addTest(api.TestResponseStatusCode())
# suite.addTest(api.TestResponseMessage())
# suite.addTest(api.TestXMLResponseMessage())
# suite.addTest(api.TestJsonResponseMessage())
# suite.addTest(api.TestQueryString())
# suite.addTest(api.TestRequest())
# suite.addTest(api.TestMethod())
# suite.addTest(base.TestBase())
# suite.addTest(base.TestItem())
# suite.addTest(base.TestCollection())
# suite.addTest(artist.TestArtist())
# suite.addTest(artist.TestArtistsCollection())
# suite.addTest(track.TestTrack())
# suite.addTest(track.TestTracksCollection())
# suite.addTest(lyrics.TestLyrics())
# suite.addTest(subtitle.TestSubtitle())
