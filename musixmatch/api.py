""" This module define the base API classes.
"""
import musixmatch
__license__ = musixmatch.__license__
__author__ = musixmatch.__author__

from urllib import urlencode, urlopen
from contextlib import contextmanager
import os
try:
    import json
except ImportError:
    import simplejson as json

try:
    from lxml import etree
except ImportError:
    try:
        import xml.etree.cElementTree as etree
    except ImportError:
        try:
            import xml.etree.ElementTree as etree
        except ImportError:
            try:
                import cElementTree as etree
            except ImportError:
                import elementtree.ElementTree as etree


class Error(Exception):
    """Base musiXmatch API error.

    >>> import musixmatch
    >>> raise musixmatch.api.Error('Error message')
    Traceback (most recent call last):
    ...
    Error: Error message
    """
    def __str__(self):
        return ': '.join(map(str, self.args))

    def __repr__(self):
        name = self.__class__.__name__
        return '%s%r' % (name, self.args)

class ResponseMessageError(Error):
    """Represents errors occurred while parsing the response messages."""

class ResponseStatusCode(int):
    """
    Represents response message status code. Casting a
    :py:class:`ResponseStatusCode` to :py:class:`str` returns the message
    associated with the status code:

    >>> from musixmatch.api import ResponseStatusCode
    >>> str(ResponseStatusCode(200))
    'The request was successful.'
    >>> str(ResponseStatusCode(401))
    'Authentication failed, probably because of a bad API key.'

    The status code to description mapping is:
    
    +------+-----------------------------------------------------------+
    | Code | Description                                               |
    +======+===========================================================+
    | 200  | The request was successful.                               |
    +------+-----------------------------------------------------------+
    | 400  | The request had bad syntax or was inherently              |
    |      | impossible to be satisfied.                               |
    +------+-----------------------------------------------------------+
    | 401  | Authentication failed, probably because of a bad API key. |
    +------+-----------------------------------------------------------+
    | 402  | A limit was reached, either you exceeded per hour         |
    |      | requests limits or your balance is insufficient.          |
    +------+-----------------------------------------------------------+
    | 403  | You are not authorized to perform this operation or       |
    |      | the api version you're trying to use has been shut down.  |
    +------+-----------------------------------------------------------+
    | 404  | Requested resource was not found.                         |
    +------+-----------------------------------------------------------+
    | 405  | Requested method was not found.                           |
    +------+-----------------------------------------------------------+

    Any other status code will produce a default message:

    >>> from musixmatch.api import ResponseStatusCode
    >>> str(ResponseStatusCode(666))
    'Unknown status code 666!'

    Casting a :py:class:`ResponseStatusCode` to :py:class:`bool` returns True if
    status code is 200, False otherwise:

    >>> from musixmatch.api import ResponseStatusCode
    >>> bool(ResponseStatusCode(200))
    True
    >>> bool(ResponseStatusCode(400))
    False
    >>> bool(ResponseStatusCode(666))
    False

    """
    __status__ = {
        200: "The request was successful.",
        400: "The request had bad syntax or was inherently " + \
             "impossible to be satisfied.",
        401: "Authentication failed, probably because of a bad API key.",
        402: "A limit was reached, either you exceeded per hour " + \
             "requests limits or your balance is insufficient.",
        403: "You are not authorized to perform this operation or " + \
             "the api version you're trying to use has been shut down.",
        404: "Requested resource was not found.",
        405: "Requested method was not found.",
    }

    def __str__(self):
        return self.__status__.get(self, 'Unknown status code %i!' % self)

    def __repr__(self):
        return 'ResponseStatusCode(%i)' % self

    def __nonzero__(self):
        return self == 200

class ResponseMessage(dict):
    """
    Abstract class which provides a base class for formatted response.
    """
    def __init__(self, response):
        raise NotImplementedError

    @property
    def status_code(self):
        """
        Is the :py:class:`ResponseStatusCode` object representing the
        message status code.
        
        :raises: :py:exc:`ValueError` if not set.
        """
        raise NotImplementedError

    def __repr__(self):
        return "%s('...')" % type(self).__name__

class JsonResponseMessage(ResponseMessage, dict):
    """
    A :py:class:`ResponseMessage` subclass which behaves like a
    :py:class:`dict` to expose the Json structure contained in the response
    message.  Parses the Json response message and build a proper python
    :py:class:`dict` containing all the information. Also, setup a
    :py:class:`ResponseStatusCode` by querying the :py:class:`dict` for the
    *['header']['status_code']* item.
    """
    def __init__(self, response):
        try:
            parsed = json.load(response)
        except Exception, e:
            raise ResponseMessageError(u'Invalid Json response message', e)
        self.update(parsed['message'])

    def __str__(self):
        s = json.dumps({ 'message': self }, sort_keys=True, indent=4)
        return '\n'.join([l.rstrip() for l in  s.splitlines()])

    @property
    def status_code(self):
        """Overload :py:meth:`ResponseMessage.status_code`"""
        return ResponseStatusCode(self['header']['status_code'])

class XMLResponseMessage(ResponseMessage, etree.ElementTree):
    """
    A :py:class:`ResponseMessage` subclass which exposes
    :py:class:`ElementTree` methods to handle XML response
    messages. Parses the XML response message and build a
    :py:class:`ElementTree` instance. Also setup the a
    :py:class:`ResponseStatusCode` by querying the *status_code* tag content.

    Casting a :py:class:`XMLResponseMessage` returns (actually re-builds) a
    pretty printed string representing the XML API response message.
    """

    def __init__(self, response):
        etree.ElementTree.__init__(self, None, response)

    def __str__(self):
        s = StringIO()
        self.wite(s)
        return s.getvalue()

    @property
    def status_code(self):
        """Overload :py:meth:`ResponseMessage.status_code`"""
        return ResponseStatusCode(self.findtext('header/status_code'))

class QueryString(dict):
    """
    A class representing  the keyword arguments to be used in HTTP requests as
    query string. Takes a :py:class:`dict` of keywords, and encode values
    using utf-8. Also, the query string is sorted by keyword name, so that its
    string representation is always the same, thus can be used in hashes.

    Casting a :py:class:`QueryString` to :py:class:`str` returns the urlencoded
    query string:

    >>> from musixmatch.api import QueryString
    >>> str(QueryString({ 'country': 'it', 'page': 1, 'page_size': 3 }))
    'country=it&page=1&page_size=3'

    Using :py:func:`repr` on :py:class:`QueryString` returns an evaluable
    representation of the current instance, excluding apikey value:

    >>> from musixmatch.api import QueryString
    >>> repr(QueryString({ 'country': 'it', 'page': 1, 'apikey': 'whatever'}))
    "QueryString({'country': 'it', 'page': '1'})"
    """
    def __init__(self, items=(), **keywords):
        dict.__init__(self, items, **keywords)
        for k in self:
            self[k] = str(self[k]).encode('utf-8')

    def __str__(self):
        return urlencode(self)

    def __repr__(self):
        query = self.copy()
        if 'apikey' in query:
            del query['apikey']
        return 'QueryString(%r)' % query

    def __iter__(self):
        """
        Returns an iterator method which will yield keys sorted by name.
        Sorting allow the query strings to be used (reasonably) as caching key.
        """
        keys = dict.keys(self)
        keys.sort()
        for key in keys:
            yield key

    def values(self):
        """Overloads :py:meth:`dict.values` using :py:meth:`__iter__`."""
        return tuple(self[k] for k in self)

    def keys(self):
        """Overloads :py:meth:`dict.keys` using :py:meth:`__iter__`."""
        return tuple(k for k in self)

    def items(self):
        """Overloads :py:meth:`dict.item` using :py:meth:`__iter__`."""
        return tuple((k, self[k]) for k in self)

    def __hash__(self):
        return hash(str(self))

    def __cmp__(self, other):
        return cmp(hash(self), hash(other))

class Method(str):
    """
    Utility class to build API methods name and call them as functions.

    :py:class:`Method` has custom attribute access to build method names like
    those specified in the API. Each attribute access builds a new Method with
    a new name.

    Calling a :py:class:`Method` as a function with keyword arguments,
    builds a :py:class:`Request`, runs it and returns the result. If **apikey**
    is undefined, environment variable **musixmatch_apikey** will be used. If
    **format** is undefined, environment variable **musixmatch_format** will be
    used. If **musixmatch_format** is undefined, jason format will be used.

    >>> import musixmatch
    >>> artist = musixmatch.api.Method('artist')
    >>> 
    >>> try:
    ...     chart = artist.chart.get(country='it', page=1, page_size=3)
    ... except musixmatch.api.Error, e:
    ...     pass
    """
    __separator__ = '.'

    def __getattribute__(self, name):
        if name.startswith('_'):
            return super(Method, self).__getattribute__(name)
        else:
            return Method(self.__separator__.join([self, name]))

    def __call__ (self, apikey=None, format=None, **query):
        query['apikey'] = apikey or musixmatch.apikey
        query['format'] = format or musixmatch.format
        return Request(self, query).response

    def __repr__(self):
        return "Method('%s')" % self
        
class Request(object):
    """
    This is the main API class. Given a :py:class:`Method` or a method name, a
    :py:class:`QueryString` or a :py:class:`dict`, it can build the API query
    URL, run the request and return the response either as a string or as a
    :py:class:`ResponseMessage` subclass. Assuming the default web services
    location, this class try to build a proper request:

    >>> from musixmatch.api import Request, Method, QueryString
    >>> method_name = 'artist.chart.get'
    >>> method = Method(method_name)
    >>> keywords = { 'country': 'it', 'page': 1, 'page_size': 3 }
    >>> query_string = QueryString(keywords)
    >>> 
    >>> r1 = Request(method_name, keywords)
    >>> r2 = Request(method_name, **keywords)
    >>> r3 = Request(method_name, query_string)
    >>> r4 = Request(method, keywords)
    >>> r5 = Request(method, **keywords)
    >>> r6 = Request(method, query_string)

    If **method** is string, try to cast it into a :py:class:`Method`. If
    **query_string** is a :py:class:`dict`, try to cast it into a
    :py:class:`QueryString`. If **query_string** is not specified, try to
    use **keywords** arguments as a :py:class:`dict` and cast it into a
    :py:class:`QueryString`.

    Turning the :py:class:`Request` into a :py:class:`str` returns the URL
    representing the API request:
    
    >>> str(Request('artist.chart.get', { 'country': 'it', 'page': 1 }))
    'http://api.musixmatch.com/ws/1.1/artist.chart.get?country=it&page=1'
    """
    def __init__ (self, api_method, query=(), **keywords):
        self.__api_method = isinstance(api_method, Method) and \
            api_method or Method(api_method)
        self.__query_string = isinstance(query, QueryString) and \
            query or QueryString(query)
        self.__query_string.update(keywords)
        self.__response = None

    @property
    def api_method(self):
        """The :py:class:`Method` instance."""
        return self.__api_method

    @property
    def query_string(self):
        """The :py:class:`QueryString` instance."""
        return self.__query_string

    @contextmanager
    def _received(self):
        """A context manager to handle url opening"""
        try:
            response = urlopen(str(self))
            yield response
        finally:
            response.close()

    @property
    def response(self):
        """
        The :py:class:`ResponseMessage` based on the **format** key in the
        :py:class:`QueryString`.
        """
        if self.__response is None:

            format = self.query_string.get('format')
            ResponseMessageClass = {
                'json': JsonResponseMessage,
                'xml': XMLResponseMessage,
            }.get(format, None)

            if not ResponseMessageClass:
                raise ResponseMessageError("Unsupported format `%s'" % format)

            with self._received() as response:
                self.__response = ResponseMessageClass(response)

        return self.__response

    def __repr__(self):
        return 'Request(%r, %r)' % (self.api_method, self.query_string)

    def __str__(self):
        return '%(ws_location)s/%(api_method)s?%(query_string)s' % {
            'ws_location': musixmatch.ws.location,
            'api_method': self.api_method,
            'query_string': self.query_string
        }

    def __hash__(self):
        return hash(str(self))

    def __cmp__(self, other):
        return cmp(hash(self), hash(other))
