"""
"""

from Products.Musixmatch import __copyright__, __license__, __docformat__, PRODUCT
from Products.CMFCore.utils import UniqueObject
from Products.CMFPlone.PloneBaseTool import PloneBaseTool
from zope.interface import Interface, implements, implementedBy
from OFS.OrderedFolder import OrderedFolder
from musixmatch.api import Method

class IMusixmatchProxy(Interface):
    """
    Musixmatch proxy interface.
    """

    def call(self, apikey, format, **keywords):
        """
        """

class MusixmatchProxy(Method, UniqueObject, PloneBaseTool):

    implements(IMusixmatchProxy)

    def __call__ (self, **keywords):
        """
        """
        return str(self.call(**keywords))

    def call(self, **keywords):
        """
        """
        if 'apikey' in keywords:
            raise BadRequest, 'apikey'
        apikey = self.getProperty('musixmatch_apikey', '') or None
        format = self.getProperty('musixmatch_format', 'json')
        return Method.__call__(self, apikey, format, **keywords)
