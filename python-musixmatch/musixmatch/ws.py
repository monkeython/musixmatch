"""
This is an utility module that provides a row musiXmatch web API interface.
Ideally it should be used like this:

>>> from musixmatch import ws
>>> it_track_chart = ws.track.chart.get(country='it', page=1, page_size=3, f_has_lyrics=1)

or 

>>> from musixmatch.ws import artist
>>> it_artist_chart = artist.chart.get(country='it', page=1, page_size=3)
"""
from musixmatch import __license__, __author__
from musixmatch import api

artist = api.Method('artist')
album = api.Method('album')
track = api.Method('track')
tracking = api.Method('tracking')
matcher = api.Method('matcher')
