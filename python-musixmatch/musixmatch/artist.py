"""
This module contains higher level classes to query Musixmatch API and build
simple dictionary-like objects representing an Artist or an ArtistsCollection.

>>> from musixmatch.artist import Artist, ArtistsCollection
>>> 
>>> artist = Artist(artist_id=292)
>>> collection = ArtistsCollection.fromChart(country=it, page=1)
"""
from musixmatch import __license__, __author__
from musixmatch import base
from musixmatch.ws import artist

class Artist(base.Item):
    """
    This class build a :py:class:`dict` like object representing an artist. It
    can get artist information through the :py:class:`musixmatch.api.Method`
    **artist.get** or from an already well-formed :py:class:`dict`. Create an
    Artist object based on a given keyword argument:

    :param   artist_id: musiXmatch artist ID
    :param artist_mbid: Musicbrainz artist ID
    :param artist_data: an already well-formed :py:class:`dict` of artist data.

    Once information are collected, the following keys are available:

    :keyword artist_id: musiXmatch artist ID
    :keyword artist_mbid: Musicbrainz artist ID
    :keyword artist_name: Artist name
    """
    __api_method__ = artist.get

class ArtistsCollection(base.ItemsCollection):
    """
    This class build a :py:class:`list` like object representing an artists
    collection. It accepts :py:class:`dict` or :py:class:`Artist` objects.
    """
    __allowedin__ = Artist

    @classmethod
    def fromSearch(cls, **keywords):
        """
        This classmethod builds an :py:class:`ArtistsCollection` from a
        **artist.search** :py:class:`musixmatch.api.Method` call.

        :param q: a string that will be searched in every data field
                     (q_track, q_artist, q_lyrics)
        :param q_track: words to be searched among track titles
        :param q_artist: words to be searched among artist names
        :param q_lyrics: words to be searched into the lyrics
        :param page: requested page of results
        :param page_size: desired number of items per result page
        :param f_has_lyrics: exclude tracks without an available lyrics
                                (automatic if q_lyrics is set)
        :param f_artist_id: filter the results by the artist_id
        :param f_artist_mbid: filter the results by the artist_mbid
        :rtype: :py:class:`ArtistsCollection`
        """
        return cls.fromResponseMessage(artist.search(**keywords))

    @classmethod
    def fromChart(cls, **keywords):
        """
        This classmethod builds an :py:class:`ArtistsCollection` from a
        **artist.chart.get** :py:class:`musixmatch.api.Method` call.

        :param page: requested page of results
        :param page_size: desired number of items per result page
        :param country: the country code of the desired country chart
        :rtype: :py:class:`ArtistsCollection`
        """
        return cls.fromResponseMessage(artist.chart.get(**keywords))

