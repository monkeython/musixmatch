"""
This module define the base API classes, and the module variable *version*
which is used to build the request URL.
"""
from musixmatch import __author__, __license__, nothing
from UserDict import UserDict
from urllib import urlencode, urlopen
from xml.dom.minidom import parseString
from contextlib import contextmanager
import sys
import os
try:
    import json
except ImportError:
    import simplejson as json

version = os.environ.get('musixmatch_apiversion', '1.1')

@contextmanager
def request(url):
    try:
        response = urlopen(url)
        yield response
    finally:
        response.close()

class Error(Exception):
    """Base musiXmatch API error."""

    def __init__(self, *args):
        self.args = tuple(args)

    def __str__(self):
        name = self.__class__.__name__
        return ': '.join(map(str, (name,) + self.args))

    def __repr__(self):
        name = self.__class__.__name__
        return '%s%r' % (name, self.args)

class ResponseError(Error):
    """Represents errors occurred while trying to get the remote resource."""

class ResponseMessageError(Error):
    """Represents errors occurred while parsing the response messages."""

class ResponseStatusCode(int):
    """
    Represents response message status code. Casting a
    :py:class:`ResponseStatusCode` to :py:class:`str` returns the message
    associated with the status code:

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

    >>> str(ResponseStatusCode(666))
    'Unknown status code 666!'

    Casting a :py:class:`ResponseStatusCode` to :py:class:`bool` returns True if
    status code is 200, False otherwise:

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
        return self.__status__.get(self,
            'Unknown status code %i!' % self)

    def __repr__(self):
        return 'ResponseStatusCode(%i)' % self

    def __nonzero__(self):
        return self == 200

class ResponseMessage(dict):
    """
    Abstract class which provides a base class for formatted response.
    """
    def __init__(self, dictionary, **keywords):
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

# class XMLResponseMessage(ResponseMessage):
#     """
#     A :py:class:`ResponseMessage` subclass which exposes
#     :py:mod:`xml.dom.minidom.Document` methods to handle XML response
#     messages.  Parses the XML response message and build a
#     :py:class:`xml.dom.minidom.Document` instance. Also setup the a
#     :py:class:`ResponseStatusCode` by querying the *status_code* tag content
#     from the :py:class:`xml.dom.minidom.Document`.
# 
#     Casting a :py:class:`XMLResponseMessage` returns (actually re-builds) a
#     pretty printed string representing the XML API response message.
#     """
#     def __init__(self, response):
#         try:
#             self.__document = parseString(response)
#             status = self.__document.getElementsByTagName('status_code')[0]
#             code = status.childNodes[0].data
#         except Exception, e:
#             raise ResponseMessageError(
#                 u'Invalid XML response message', e)
#         self._status_code = ResponseStatusCode(code)
# 
#     def __str__(self):
#         message = self.__document.getElementsByTagName('message')[0]
#         s = message.toprettyxml(4 * ' ')
#         return '\n'.join([ l for l in s.splitlines() if l.strip() ])
# 
#     def __getattribute__(self, name):
#         """
#         Customize class beviour by passing any attribute access request to
#         internal :py:class:`xml.dom.minidom.Document` instance.
#         """
#         if name.startswith('_') or name == 'getResponseStatusCode':
#             return super(XMLResponseMessage, self).__getattribute__(name)
#         else:
#             return getattr(self.__document, name)
# 
# class JsonpResponseMessage(ResponseMessage):
#     pass

class JsonResponseMessage(ResponseMessage, dict):
    """
    A :py:class:`ResponseMessage` subclass which behaves like a
    :py:class:`dict` to expose the Json structure contained in the response
    message.  Parses the Json response message and build a proper python
    :py:class:`dict` containing all the informations. Also, setup a
    :py:class:`ResponseStatusCode` by querying the :py:class:`dict` for the
    *['header']['status_code']* item.
    """
    def __init__(self, response):
        try:
            parsed = json.loads(response)
        except Exception, e:
            raise ResponseMessageError(
                u'Invalid Json response message', e)
        self.update(parsed['message'])

    def __str__(self):
        s = json.dumps({ 'message': self }, sort_keys=True, indent=4)
        return '\n'.join([l.rstrip() for l in  s.splitlines()])

    @property
    def status_code(self):
        """Overload :py:meth:`ResponseMessage.status_code`"""
        return ResponseStatusCode(self['header']['status_code'])

class QueryString(dict):
    """
    A class representing  the keyword arguments to be used in HTTP requests as
    query string. Takes a :py:class:`dict` of keywords, and encode values
    using utf-8. Also, the query string is sorted by keyword name, so that its
    string representation is always the same, thus can be used in hashes.

    Casting a :py:class:`QueryString` to :py:class:`str` returns the urlencoded
    query string:

    >>> str(QueryString({ 'country': 'it', 'page': 1, 'page_size': 3 }))
    'country=it&page=1&page_size=3'

    Using :py:func:`repr` on :py:class:`QueryString` returns an evaluable
    representation of the current instance, excluding apikey value:

    >>> repr(QueryString({ 'country': 'it', 'page': 1, 'apikey': 'whatever'}))
    "QueryString({'country': 'it', 'page': 1})"
    """
    def __init__(self, items={}, **keywords):
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

    Calling a :py:class:`Method` as a function with positional
    arguments, builds a :py:class:`Request`, runs it and returns the result.
    It uses itself to determin the API method name and version, and the
    *keywords* arguments for the query string. If **apikey** is
    undefined, environment variable **musixmatch_apikey** will be used. If
    **format** is undefined, environment variable **musixmatch_format**
    will be used. If **musixmatch_format** is undefined, jason format will
    be used.

    >>> artist = Method('artist')
    >>> 
    >>> chart = artist.chart.get(country='it', page=1, page_size=3)
    """

    def __getattribute__(self, name):
        if name.startswith('_'):
            return super(Method, self).__getattribute__(name)
        else:
            return Method('.'.join([self, name]))

    def __call__ (self, apikey=None, format=None, **keywords):
        if apikey is None:
            apikey = os.environ.get('musixmatch_apikey')
        keywords.setdefault('apikey', apikey)
        if format is None:
            format = os.environ.get('musixmatch_format', 'json')
        keywords.setdefault('format', format)
        _request = Request(self, keywords)
        return _request.getResponseMessage()

    def __repr__(self):
        return "Method('%s')" % self
        
class Request(object):
    """
    This is the main API class. Given a :py:class:`Method` or a method name, a
    :py:class:`QueryString` or a :py:class:`dict`, it can build the API query
    URL, run the request and return the resposne either as a string or as a
    :py:class:`ResponseMessage` subclass. Assuming the default api version, this
    class try to build a proper request:

    >>> method_name = 'artist.chart.get'
    >>> method = Method(method_name)
    >>> keywords = { 'country': 'it', 'page': 1, 'page_size': 3 }
    >>> query_string = QueryString(keywords)
    >>> 
    >>> r1 = Request(method_name, keywords)
    >>> r2 = Request(method_name, **keywords)
    >>> r3 = Request(method_name, query_string)
    >>> r4 = Request(method, keywords}
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
    'http://api.musixmatch.com/ws/1.1/artist.chart.get?apikey=None&country=it&page=1'

    API version is determined as follow:

    1. if environment varaible **musixmatch_apiversion** is defined, it is used.
    2. if no environment variable is defined, version is guessed from arguments.
    3. if version argument is not defined, default is used.
    """
    def __init__ (self, api_method, query_string={}, **keywords):
        if not isinstance(query_string, QueryString):
            query_string = QueryString(query_string)
        if not isinstance(api_method, Method):
            api_method = Method(api_method)
        query_string.update(keywords)
        self.__api_method = api_method
        self.__query_string = query_string
        self.__response = None

    @property
    def api_method(self):
        """The :py:class:`Method` instance."""
        return self.__api_method

    @property
    def query_string(self):
        """The :py:class:`QueryString` instance."""
        return self.__query_string

    def getResponse(self):
        """
        Run the requsts and collects the response message as a
        :py:class:`string`.
        """

        if self.__response is None:
            url = str(self)
            try:
                self.__response = urlopen(url).read()
            except Exception, e:
                raise Error(u'Could not open API URL %s: %s' %  (url, e))
        return self.__response

    def getResponseMessage(self):
        """
        Returns a proper :py:class:`ResponseMessage` based on the **format**
        key in the :py:class:`QueryString`.
        """
        ResponseMessageClass = {
            'json': JsonResponseMessage,
        #    'xml': XMLResponseMessage,
        }.get(self.query_string.get('format'), None)
        if ResponseMessageClass:
            return ResponseMessageClass(self.getResponse())
        else:
            raise ResponseMessageError("Unsupported format `%s'" % format)

    def __repr__(self):
        return 'Request(%r, %r)' % (self.api_method, self.query_string)

    def __str__(self):
        return 'http://api.musixmatch.com/ws/%s/%s?%s' % (
            version, self.api_method, self.query_string )

    def __hash__(self):
        return hash(str(self))

    def __cmp__(self, other):
        return cmp(hash(self), hash(other))
