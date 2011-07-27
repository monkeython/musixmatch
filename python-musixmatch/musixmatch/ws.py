"""
This is an utility module that provides a row musiXmatch web API interface.
Ideally it should be used like this:

>>> import musixmatch
>>> 
>>> try:
...     chart = musixmatch.ws.track.chart.get(country='it', f_has_lyrics=1)
... except musixmatch.api.Error, e:
...     pass
"""
from warnings import warn
import os
import musixmatch
__license__ = musixmatch.__license__
__author__ = musixmatch.__author__

_version = os.environ.get('musixmatch_apiversion', None)
if not _version:
    _version = '1.1'
else:
    warn("Use of `musixmatch_apiversion' was deprecated in favour of `musixmatch_wslocation'", DeprecationWarning)

location = os.environ.get('musixmatch_wslocation', 'http://api.musixmatch.com/ws/%s' % _version)

artist = musixmatch.api.Method('artist')
album = musixmatch.api.Method('album')
track = musixmatch.api.Method('track')
tracking = musixmatch.api.Method('tracking')
matcher = musixmatch.api.Method('matcher')
