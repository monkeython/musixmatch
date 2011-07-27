import unittest
from musixmatch import *
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class TestError(unittest.TestCase):

    def test__str__(self):
        error = api.Error('test error', Exception('test exception'))
        self.assertEqual(str(error), 'test error: test exception')

class TestResponseStatusCode(unittest.TestCase):

    def test__init__(self):
        self.assertRaises(ValueError, api.ResponseStatusCode, 'fail')

        self.assertRaises(TypeError, api.ResponseStatusCode, [1,2,3])

    def test__int__(self):
        self.assertEqual(int(api.ResponseStatusCode('1')), 1)

    def test__str__(self):
        self.assertEqual(str(api.ResponseStatusCode('200')),
            'The request was successful.')

        self.assertEqual(str(api.ResponseStatusCode('-1')),
            'Unknown status code -1!')

    def test__nonzero__(self):
        self.assertEqual(bool(api.ResponseStatusCode('200')), True)
        self.assertEqual(bool(api.ResponseStatusCode('404')), False)

class TestResponseMessage(unittest.TestCase):

    def test__init__(self):
        self.assertRaises(NotImplementedError, api.ResponseMessage, '')

class TestXMLResponseMessage(unittest.TestCase):

    message = """<message>
    <header>
        <status_code>200</status_code>
    </header>
    <body>
    </body>
</message>"""

    def test_status_code(self):
        message = api.XMLResponseMessage(StringIO(self.message))
        self.assertEqual(isinstance(message.status_code, api.ResponseStatusCode), True)

class TestJsonResponseMessage(unittest.TestCase):
    message = """{"message":{
    "header":{
        "status_code":200},
    "body":{
}}}"""

    def test_status_code(self):
        message = api.JsonResponseMessage(StringIO(self.message))
        self.assertEqual(isinstance(message.status_code, api.ResponseStatusCode), True)

class TestQueryString(unittest.TestCase):
    def test__str__(self):
        keywords = { 'country': 'it', 'page': 1, 'page_size': 3 }
        query_string = api.QueryString(keywords)
        self.assertEqual(str(query_string), 'country=it&page=1&page_size=3')
    def test__repr__(self):
        keywords = { 'apikey': 'it', 'id': 12345, 'format': 'json' }
        query_string = api.QueryString(keywords)
        self.assertEqual(repr(query_string).count('apikey'), 0)

class TestRequest(unittest.TestCase):
    def test__str__(self):
        url = 'http://api.musixmatch.com/ws/1.1/test?apikey=apikey&format=format'.encode('utf-8')
        method = api.Method('test')
        query_string = api.QueryString({'apikey':'apikey','format':'format'})
        request = api.Request(method, query_string)
        self.assertEqual(str(request), url)

class TestMethod(unittest.TestCase):

    def test__getattribute__(self):
        method = api.Method('test')
        self.assertEqual(hasattr(method, 'subtest'), True)
        self.assertEqual(hasattr(method, '__nothing__'), False)

if __name__ == '__main__':
    unittest.main()
