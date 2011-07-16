"""
This module contains higher level classes to query Musixmatch API and build
simple dictionary-like objects representing a Track or a TracksCollection.

>>> from musixmatch.track import Track, TracksCollection
>>> 
>>> track = Track(track_mbid=8976)
>>> collection = TracksCollection.fromChart(country=us, page=1)
"""
from musixmatch import __license__, __author__
from musixmatch import api, base, lyrics, subtitle
from musixmatch.ws import track, matcher, album

_marker=object()

class Track(base.Item):
    """
    This class builds a :py:class:`dict` like object representing a track. It
    can get track information through the :py:class:`musixmatch.api.Method`
    **track.get** or from an already well-formed :py:class:`dict`. Create a
    Track object based on a given keyword argument:

    :param track_id: musiXmatch track ID
    :param musicbrainz_id: Musicbrainz track ID
    :param track_echonest_id: Echonest track ID
    :param track_data: an already well-formed :py:class:`dict` of track data
    :raises: :py:exc:`musixmatch.api.Error` if :py:class:`musixmatch.api.ResponseStatusCode` is not 200

    Once information are collected, the following keys are available:

    :keyword track_id: musiXmatch track ID
    :keyword track_mbid: Musicbrainz track ID
    :keyword lyrics_id: musiXmatch lyrics ID
    :keyword instrumental: wether the track is instrumental or not
    :keyword subtitle_id: musiXmatch subtitle ID
    :keyword track_name: track name
    :keyword album_coverart_100x100: album cover URL
    :keyword artist_id: musiXmatch artist ID
    :keyword artist_mbid: Musicbrainz artist ID
    :keyword artist_name: artist name

    Keyword access have been overloaded thanks to the :py:meth:`get` method
    which will eventually fetch the matching lyrics or subtitle.
    """
    __api_method__ = track.get
    
    @classmethod
    def fromMatcher(cls, **keywords):
        """
        Returns a :py:class:`Track` based on the result of the
        :py:class:`musiXmatch.api.Method` **matcher.track.get**. Accepts the
        following keywords:

        :param q_track: words to be searched among track titles
        :param q_artist: words to be searched among artist names
        """
        return cls.fromResponseMessage(matcher.track.get(**keywords))

    def get(self, key, default=_marker):
        """
        If key is *lyrics* or *subtitle* try to query api for proper value,
        and build an :py:class:`musixmatch.lyrics.Lyrics` or
        :py:class:`musixmatch.subtitle.Subtitle`. Access to the above mentioned
        keys may fail with :py:exc:`musixmatch.api.Error`. Once fetched, the
        result is saved.
        """
        special = {
            'lyrics': lyrics.Lyrics,
            'subtitle': subtitle.Subtitle,
        }
        if key in special and not key in self:
            self[key] = special[key](track_id=self['track_id'])
        value = dict.get(self, key, default)
        if value == _marker:
            raise KeyError, key
        return value

    def __getitem__(self, key):
        return self.get(key)

    def postFeedback(self, feedback):
        """
        Post feedback about lyrics for this track. **feedback** can be one of:

        :keyword wrong_attribution: the lyrics shown are not by the artist that
                                    I selected.
        :keyword bad_characters:    there are strange characters and/or words
                                    that are partially scrambled.
        :keyword lines_too_long:    the text for each verse is too long!
        :keyword wrong_verses:      there are some verses missing from the
                                    beginning or at the end.
        :keyword wrong_formatting:  the text looks horrible, please fix it!
        """
        accepted = [
            'wrong_attribution', 'bad_characters', 'lines_too_long',
            'wrong_verses', 'wrong_formatting' ]
        if feedback in accepted:
            message = track.lyrics.feedback.post(
                track_id=self['track_id'],
                lyrics_id=self['track_id']['lyrics']['lyrics_id'],
                feedback=feedback
            )
            if not message.status_code:
                raise api.Error(str(message.status_code))
        else:
            raise TypeError, '%r not in %r' % (feedback, accepted)

class TracksCollection(base.ItemsCollection):
    """
    This class build a :py:class:`list` like object representing a tracks
    collection. It accepts :py:class:`dict` or :py:class:`Track` objects.
    """
    __allowedin__ = Track

    @classmethod
    def fromAlbum(cls, **keywords):
        """
        This classmethod builds an :py:class:`TracksCollection` from a
        **album.tracks.get** :py:class:`musixmatch.api.Method` call.

        :param album_id: musiXmatch album ID
        """
        return cls.fromResponseMessage(album.tracks.get(**keywords))

    @classmethod
    def fromSearch(cls, **keywords):
        """
        This classmethod builds an :py:class:`TracksCollection` from a
        **track.search** :py:class:`musixmatch.api.Method` call.

        :param q: a string that will be searched in every data field
                  (q_track, q_artist, q_lyrics)
        :param q_track: words to be searched among track titles
        :param q_artist: words to be searched among artist names
        :param q_track_artist: words to be searched among track titles or
                               artist names
        :param q_lyrics: words to be searched into the lyrics
        :param page: requested page of results
        :param page_size: desired number of items per result page
        :param f_has_lyrics: exclude tracks without an available lyrics
                             (automatic if q_lyrics is set)
        :param f_artist_id: filter the results by the artist_id
        :param f_artist_mbid: filter the results by the artist_mbid
        :param quorum_factor: only works together with q and q_track_artist
                              parameter. Possible values goes from 0.1 to
                              0.9. A value of 0.9 means: 'match at least 90
                              percent of the words'.
        """
        return cls.fromResponseMessage(track.search(**keywords))

    @classmethod
    def fromChart(cls, **keywords):
        """
        This classmethod builds an :py:class:`TracksCollection` from a
        **track.chart.get** :py:class:`musixmatch.api.Method` call.

        :param page: requested page of results
        :param page_size: desired number of items per result page
        :param country: the country code of the desired country chart
        :param f_has_lyrics: exclude tracks without an available lyrics
                             (automatic if q_lyrics is set)
        """
        return cls.fromResponseMessage(track.chart.get(**keywords))
