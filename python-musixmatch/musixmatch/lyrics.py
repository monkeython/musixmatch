"""
This module contains higher level classes to query Musixmatch API and build
simple dictionary-like objects representing a track lyrics.

>>> from musixmatch.lyrics import Lyrics
>>> 
>>> lyrics = Lyrics(lyrics_id=292)
"""
from musixmatch import __license__, __author__
from musixmatch import base
from musixmatch.ws import track

class Lyrics(base.Item):
    """
    This class builds a :py:class:`dict` object representing a the lirycs of a
    track. It can get lyrics through the :py:class:`musixmatch.api.Method`
    **track.lyrics.get** or from an already well-formed :py:class:`dict`.
    Create a Track object based on a given keyword argument:

    :param track_id: musiXmatch track ID
    :param musicbrainz_id: Musicbrainz track ID
    :param track_echonest_id: Echonest track ID
    :param lyrics_data: an already well-formed :py:class:`dict` of track data
    :raises: :py:class:`musixmatch.api.Error` if :py:class:`musixmatch.api.ResponseMessageError` is not 200

    Once informations are collected, the following keys are available:

    :keyword lyrics_body: the lyrics text
    :keyword lyrics_id: the Musixmatch lyrics id
    :keyword lyrics_language: the lyrics language
    :keyword lyrics_copyright: the lyrics copyright statement
    :keyword pixel_tracking_url: the pixel tracking url
    :keyword script_tracking_url: the script tracking url
    """
    __api_method__ = track.lyrics.get

