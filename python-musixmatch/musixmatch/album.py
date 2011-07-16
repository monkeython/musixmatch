"""
This module contains higher level classes to query Musixmatch API and build
simple dictionary-like objects representing an Album or an AlbumsCollection.

>>> from musixmatch.album import Album, AlbumsCollection
>>> 
>>> album = Album(album_id=292)
>>> collection = AlbumsCollection.fromArtist(country=it, page=1)
"""
from musixmatch import __license__, __author__
from musixmatch import base
from musixmatch.ws import album, artist

class Album(base.Item):
    """
    This class build a :py:class:`dict` like object representing an album. It
    can get album information through the :py:class:`musixmatch.api.Method`
    **album.get** or from an already well-formed :py:class:`dict`. Create an
    Album object based on a given keyword argument:

    :param   album_id: musiXmatch album ID
    :param album_data: an already well-formed :py:class:`dict` of album data.

    Once information are collected, the following keys are available:

    :keyword album_id: musiXmatch album ID
    :keyword album_name: album name
    :keyword album_release_date: album release date
    :keyword album_release_type: type of the album
    :keyword album_coverart_100x100: coverart URL
    :keyword artist_id: album artist musiXmatch ID
    :keyword artist_name: album artist name
    """
    __api_method__ = album.get

class AlbumsCollection(base.ItemsCollection):
    """
    This class build a :py:class:`list` like object representing an albums
    collection. It accepts :py:class:`dict` or :py:class:`Album` objects.
    """
    __allowedin__ = Album

    @classmethod
    def fromArtist(cls, **keywords):
        """
        This classmethod builds an :py:class:`AlbumsCollection` from a
        **artist.albums.get** :py:class:`musixmatch.api.Method` call.

        :param artist_id: album artist musiXmatch ID
        :param g_album_name: group albums by name
        :param s_release_date: sort albums by release date
        :rtype: :py:class:`AlbumsCollection`
        """
        return cls.fromResponseMessage(artist.albums.get(**keywords))

