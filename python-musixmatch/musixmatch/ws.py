"""
This is an utility module that provides a row musiXmatch web API interface.
Ideally it should be used like this:

>>> import musixmatch.ws
>>> import musixmatch.api
>>> 
>>> try:
...     chart = musixmatch.ws.track.chart.get(country='it', f_has_lyrics=1)
... except musixmatch.api.Error, e:
...     pass

or 

>>> from musixmatch.ws import artist
>>> import musixmatch.api
>>> try:
...     chart = artist.chart.get(country='us')
... except musixmatch.api.Error, e:
...     pass
"""
import musixmatch
__license__ = musixmatch.__license__
__author__ = musixmatch.__author__

from musixmatch import api

artist = api.Method('artist')
album = api.Method('album')
track = api.Method('track')
tracking = api.Method('tracking')
matcher = api.Method('matcher')
