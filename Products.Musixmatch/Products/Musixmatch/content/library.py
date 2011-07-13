"""
"""

from Products.ATContentTypes.content.folder import ATFolder
from Products.Archetypes.BaseContent import BaseSchema
from Products.Archetypes.Field import IntergerField
from Products.Archetypes.Widget import IntegerWidget
from Products.Archetypes.public import registerType, Schema
from zope.interface import implements, implementedBy
from Products.Musixmatch.content.interfaces import ILibrary
from Products.Musixmatch import __copyright__, __license__, __docformat__, PRODUCT


class MusixmatchLibrary(ATFolder):
    """
    """

    implements(ILibrary, *implementedBy(ATFolder))
    schema = BaseSchema.copy() + Schema((
        IntergerField(
            name='library_id',
            widget=IntegerWidget(
                label="Musixmatch Library ID",
                label_msgid='Musixmatch_Library_label',
                description = "Library ID within the Musixmatch database",
                i18n_domain='Musixmatch',
                visible = {"new": "invisible", "edit": "invisible"},
            ),
            required=False
        )
    ))

    def addArtist(self, artist_id):
        return artist.addArtist(self, artist_id)

    def addAlbum(self, album_id, artist_id):
        self.addArtist(artist_id)
        return album.addAlbum(getattr(self, artist_id), album_id)

    def addTrack(self, track_id, album_id, artist_id):
        self.addAlbum(album_id, artist_id)
        return track.addTrack(getattr(getattr(self, artist_id), album_id), track)

registerType(Library, PRODUCT)
