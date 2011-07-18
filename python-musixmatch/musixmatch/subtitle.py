"""
This module contains higher level classes to query Musixmatch API and build
simple dictionary-like objects representing a track subtitle.

>>> from musixmatch.subtitle import Subtitle
>>> 
>>> subtitle = Subtitle(subtitle_id=292)
"""
import musixmatch
__license__ = musixmatch.__license__
__author__ = musixmatch.__author__

from musixmatch.base import Item
from musixmatch.ws import track

class Subtitle(Item):
    """
    This class builds a :py:class:`dict` object representing a subtitle of a
    track. It can get subtitle through the :py:class:`musixmatch.api.Method`
    **track.subtitle.get** or from an already well-formed :py:class:`dict`.
    Create a Track object based on a given keyword argument:

    :param track_id: musiXmatch track ID
    :param musicbrainz_id: Musicbrainz track ID
    :param track_echonest_id: Echonest track ID
    :param subtitle_data: an already well-formed :py:class:`dict` of track data
    :raises: :py:class:`musixmatch.api.Error` if :py:class:`musixmatch.api.ResponseMessageError` is not 200

    Once information are collected, the following keys are available:

    :keyword subtitle_body: the subtitle text
    :keyword subtitle_id: the Musixmatch subtitle id
    :keyword subtitle_language: the subtitle language
    """
    __api_method__ = track.subtitle.get

