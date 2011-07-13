import unittest
from musixmatch import api

class TestError(unittest.TestCase):

    def test__str__(self):
        error = api.Error('test error', Exception('test exception'))
        self.assertEqual(str(error), 'Error: test error: test exception')

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

# class TestXMLResponseMessage(unittest.TestCase):
# 
#     __successful = """<message>
#     <header>
#         <status_code>200</status_code>
#     </header>
#     <body>
#     </body>
# </message>"""
#     __not_found = """<message>
#     <header>
#         <status_code>404</status_code>
#     </header>
#     <body>
#     </body>
# </message>"""
#     def test__init__(self):
#         self.assertRaises(api.ResponseMessageError,
#             api.XMLResponseMessage, '')
#         self.assertRaises(api.ResponseMessageError,
#             api.XMLResponseMessage, None)
#         self.assertRaises(api.ResponseMessageError,
#             api.XMLResponseMessage, 'fail')
# 
#     def test__str__(self):
#         message = str(api.XMLResponseMessage(self.__successful))
#         self.assertEqual(message, str(api.XMLResponseMessage(message)))
# 
#     def test__getattribute__(self):
#         message = api.XMLResponseMessage(self.__successful)
#         self.assertEqual(hasattr(message, 'getElementsByTagName'), True)
# 
#     def test_getResponseStatusCode(self):
#         message = api.XMLResponseMessage(self.__successful)
#         code = message.getResponseStatusCode()
#         self.assertEqual(isinstance(code, api.ResponseStatusCode), True)
#         self.assertEqual(int(code), 200)

class TestJsonResponseMessage(unittest.TestCase):
    __successful = """{"message":{
    "header":{
        "status_code":200},
    "body":{
}}}"""
    __not_found = """{"message":{
    "header":{
        "status_code":404},
    "body":{
}}}"""
    def test__init__(self):
        self.assertRaises(api.ResponseMessageError,
            api.JsonResponseMessage, '')
        self.assertRaises(api.ResponseMessageError,
            api.JsonResponseMessage, None)
        self.assertRaises(api.ResponseMessageError,
            api.JsonResponseMessage, 'fail')

    def test__str__(self):
        message = str(api.JsonResponseMessage(self.__successful))
        self.assertEqual(message, str(api.JsonResponseMessage(message)))

    def test__getitem__(self):
        message = api.JsonResponseMessage(self.__successful)
        self.assertEqual(bool(message.get('header')), True)

    def test_status_code(self):
        message = api.JsonResponseMessage(self.__successful)
        code = message.status_code
        self.assertEqual(isinstance(code, api.ResponseStatusCode), True)
        self.assertEqual(int(code), 200)

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
