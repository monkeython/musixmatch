"""
This module contains tha base classes for the Musixmatch API generated content:

* :py:class:`musixmatch.artist.Artist`
* :py:class:`musixmatch.track.Track`
* :py:class:`musixmatch.lyrics.Lyrics`
* :py:class:`musixmatch.subtitle.Subtitle`
"""
from musixmatch import __license__, __author__
from musixmatch import api
import random
import sys
import pprint

class Base(object):
    """
    The very base (abstract) class of the musixmatch package. I want all
    classes to implement :py:meth:`__str__` and :py:meth:`__repr__`.

    Casting an :py:class:`Base` into a :py:class:`str` returns a pretty printed
    (maybe using :py:mod:`pprint`) string representing the object.

    Using :py:func:`repr` on an :py:class:`Base` returns an evaluable string
    representing the instance, whenever it is reasonable.

    :py:class:`Base` instances are hashable.
    """

    @classmethod
    def label(self):
        """
        Returns the label that should be used as keyword in the
        :py:class:`musixmatch.api.JsonResponseMessage` body.
        """
        return getattr(self, '__label__', self.__name__.lower())

    @classmethod
    def apiMethod(self):
        """
        Returns the :py:class:`musixmatch.api.Method` that should be used to
        build the object. Defaults to *label.get* where *label* is the result
        from :py:meth:`label`
        """
        api_method = getattr(self, '__api_method__', '%s.%s' % (self.label(),'get'))
        if not isinstance(api_method, api.Method):
            api_method = api.Method(str(api_method))
        return api_method

    def __str__(self):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError

class Item(Base, dict):
    """
    This is the base class for any entity in musixmatch package. Even if
    response messages may have XML format, the JSON representation will be the
    main data format, so the :py:class:`dict` sounds like the best base class.
    It fetches the item data by guessing the :py:class:`musixmatch.api.Method`
    and building the query based on a given keyword argument. Positional
    argument is meant to be used by collection classes. Use only keyword
    arguments.
    """
    __api_method__ = None

    def __init__(self, dictionary=None, **keywords):
        if dictionary:
            dict.update(self, dictionary)
        elif keywords:
            message = self.apiMethod()(**keywords)
            dict.update(self, type(self).fromResponseMessage(message))

    def __str__(self):
        return pprint.pformat(dict(self),4,1)

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, dict(self))

    def __hash__(self):
        return int(self['%s_id' % type(self).label()])

    @classmethod
    def fromResponseMessage(self, message):
        """
        Returns an object instance, built from a
        :py:class:`musixmatch.api.ResponseMessage`
        """
        if not message.status_code:
            raise api.Error(str(message.status_code))
        return self.fromDiconary(message['body'][self.label()])

    @classmethod
    def fromDiconary(self, dictionary, **keywords):
        """
        Returns an object instance, built from a :py:class:`dict`
        """
        item = self()
        dict.update(item, dictionary, **keywords)
        return item

class ItemsCollection(Base, list):
    """
    This is the base class for collections of items, like search results, or
    charts. It behaves like :py:class:`list`, but enforce new items to be
    instance of appropriate class checking against :py:meth:`allowedin`.
    """

    __allowedin__ = Item

    def __init__(self, *items):
        self.extend(items)

    def __repr__(self):
        items = [ repr(i) for i in self ]
        return '%s(%s)' % (type(self).__name__, ', '.join(items))

    def __str__(self):
        return list.__str__(self)

    def __add__(self, iterable):
        collection = self.copy()
        collection.extend(iterable)
        return collection

    def __iadd__(self, iterable):
        raise NotImplementedError

    def __mul__(self, by):
        raise NotImplementedError

    def __imul__(self, by):
        raise NotImplementedError

    def __setitem__(self, key, item):
        raise NotImplementedError

    def __setslice__(self, *indices):
        raise NotImplementedError

    def __getslice__(self, i=0, j=-1):
        return self.__getitem__(slice(i,j))

    def __getitem__(self, i):
        if type(i) is int:
            return list.__getitem__(self, i)
        elif type(i) is slice:
            collection = type(self)()
            list.extend(collection, list.__getitem__(self, i))
            return collection
        else:
            raise TypeError, i

    def append(self, item):
        self.insert(len(self), item)

    def extend(self, iterable):
        for item in iterable:
            self.append(item)

    def count(self, item):
        return int(item in self)

    def copy(self):
        """Returns a shallow copy of the collection."""
        collection = type(self)()
        list.extend(collection, self)
        return collection

    def index(self, item, *indices):
        return list.index(self, item, *indices[:2])

    def insert(self, key, item):
        allowed = self.allowedin()
        if not isinstance(item, allowed):
            item = allowed.fromDiconary(item)
        if not item in self:
            list.insert(self, key, item)

    def paged(self, page_size=3):
        """
        Returns self, paged by **page_size**. That is, a list of
        sub-collections which contain "at most" **page_size** items.
        """
        return [ self.page(i,page_size)
            for i in range(self.pages(page_size)) ]

    def page(self, page_index, page_size=3):
        """
        Returns a specific page, considering pages that contain "at most"
        **page_size** items.
        """
        page = type(self)()
        i = page_index * page_size
        list.extend(page, self[i:i+page_size])
        return page

    def pager(self, page_size=3):
        """
        A generator of pages, considering pages that contain "at most"
        **page_size** items.
        """
        for i in xrange(self.pages(page_size)):
            yield self.page(i, page_size)
    
    def pages(self,page_size=3):
        """
        Returns the number of pages, considering pages that contain "at most"
        **page_size** items.
        """
        pages, more = divmod(len(self), page_size)
        return more and pages + 1 or pages

    @classmethod
    def fromResponseMessage(self, message):
        """
        Returns an object instance, built on a
        :py:class:`musixmatch.api.ResponseMessage`
        """
        if not message.status_code:
            raise api.Error(str(message.status_code))
        list_label = self.label()
        item_label = self.allowedin().label()
        items = [ i[item_label] for i in message['body'][list_label] ]
        return self(*items)

    @classmethod
    def allowedin(self):
        """
        Returns the allowed content class. Defaults to :py:class:`Item`
        """
        return self.__allowedin__

    @classmethod
    def label(self):
        item_name = self.allowedin().label()
        return '%s_list' % item_name

