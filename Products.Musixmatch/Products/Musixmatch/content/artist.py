"""
"""

from Products.ATContentTypes.content.folder import ATFolder
from Products.Archetypes.BaseContent import BaseSchema
from Products.Archetypes.Field import IntergerField
from Products.Archetypes.Widget import IntegerWidget
from Products.Archetypes.public import registerType, Schema
from zope.interface import implements, implementedBy
from Products.Musixmatch.content.interfaces import IArtist
from Products.Musixmatch import __copyright__, __license__, __docformat__, PRODUCT


class MusixmatchArtist(ATFolder):
    """
    """

    implements(IArtist, *implementedBy(ATFolder))
    schema = BaseSchema.copy() + Schema((
        IntergerField(
            name='artist_id',
            widget=IntegerWidget(
                label="Musixmatch Artist ID",
                label_msgid='Musixmatch_Artist_label',
                description = "Artist ID within the Musixmatch database",
                i18n_domain='Musixmatch',
                visible = {"new": "invisible", "edit": "invisible"},
            ),
            required=False
        )                                             
    ))

registerType(Artist, PRODUCT)
