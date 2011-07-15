import unittest
from musixmatch import base
from musixmatch import api

class TestBase(unittest.TestCase):

    Class = base.Base
    def test_label(self):
        self.assertEqual(self.Class.label(), self.Class.__name__.lower())

class TestItem(TestBase):
    Class = base.Item
    item = { "item_id": "9673" }
    item_str = "{   'item_id': '9673'}"
    item_repr = "Item({'item_id': '9673'})"
    item_hash = 9673
    item_id = 'item_id'

    # def test_fromResponseMessage(self):
    #     self.assertRaises(api.Error,
    #         self.Class.fromResponseMessage, self.fail)
    #     success = self.Class.fromResponseMessage(self.success)
    #     self.assertEqual(success[item_id],
    #         self.success['body'][self.label()][self.item_id])
    def test_fromDiconary(self):
        item = self.Class.fromDictionary(self.item)
        # Data integrity
        for k in self.item.keys():
            self.assertEqual(item[k], self.item[k])

    def test__str__(self):
        item = self.Class.fromDictionary(self.item)
        self.assertEqual(str(item),self.item_str)

    def test__repr__(self):
        item = self.Class.fromDictionary(self.item)
        self.assertEqual(repr(item),self.item_repr)

    def test__hash__(self):
        item = self.Class.fromDictionary(self.item)
        self.assertEqual(hash(item), self.item_hash)

class TestCollection(unittest.TestCase):

    Class = base.ItemsCollection
    AllowedContent = base.ItemsCollection.allowedin()
    item_list = 'item_list'
    item_id = 'item_id'
    item = 'item'
    message = {
        "body": {
            "item_list": [
                {
                    "item": {
                        "item_id": "292",
                        "item_name": "item_292"
                    }
                },
                {
                    "item": {
                        "item_id": "8976",
                        "item_name": "item_8976"
                    }
                },
                {
                    "item": {
                        "item_id": "9673",
                        "item_name": "item_9673"
                    }
                }
            ]
        },
        "header": {
            "execute_time": 0.14144802093506001,
            "status_code": 200
        }
    }

    def test_insert(self):
        collection = self.Class()
        saved = self.message['body'][self.item_list][0][self.item]
        item = self.AllowedContent(saved)
        collection.insert(0, item)
        # Item correctly inserted
        self.assertEqual(collection[0], item)

        saved = self.message['body'][self.item_list][1][self.item]
        collection.insert(0, saved)
        # Item corectly casted to self.AllowedContent
        self.assertEqual(type(collection[0]), self.AllowedContent)
        # Item content integrity
        self.assertEqual(collection[0][self.item_id], saved[self.item_id])
        # Previously inserted item has shifted position
        self.assertEqual(collection[1], item)

    def test_append(self):
        collection = self.Class()
        saved = self.message['body'][self.item_list][1][self.item]
        item = self.AllowedContent.fromDictionary(saved)
        collection.append(item)
        # Item correctly appended
        self.assertEqual(collection[0], item)

        saved = self.message['body'][self.item_list][2][self.item]
        collection.append(saved)
        # Item correctly appended
        self.assertEqual(collection[1][self.item_id], saved[self.item_id])

        saved = self.message['body'][self.item_list][0][self.item]
        collection.append(saved)
        # Item corectly casted to self.AllowedContent
        self.assertEqual(type(collection[2]), self.AllowedContent)
        # Item content integrity
        self.assertEqual(collection[2][self.item_id], saved[self.item_id])

    def test_extend(self):
        items = [ i[self.item] for i in self.message['body'][self.item_list] ]
        collection = self.Class(self.AllowedContent(items[0]))
        self.assertEqual(type(collection[0]), self.AllowedContent)
        typed = [ self.AllowedContent(i) for i in items[1:] ]
        for i in typed:
            self.assertEqual(type(i), self.AllowedContent)
        collection.extend(typed)
        # Collection correctly extended
        self.assertEqual(collection[1], typed[0])
        self.assertEqual(collection[2], typed[1])

        row = items[:2] + items[1:3]
        collection.extend(row)
        # Items content integrity: no duplicate
        self.assertEqual(len(collection), 3)

        collection = self.Class()
        collection.extend(row)
        self.assertEqual(len(row), 4)
        self.assertEqual(len(collection), 3)
        # Items corectly casted to self.AllowedContent
        for i in range(3):
            self.assertEqual(type(collection[i]), self.AllowedContent)

    # def test__setitem__(self):
    #     collection = self.Class(self.AllowedContent(
    #         self.message['body'][self.item_list][1][self.item]))
    #     saved = self.message['body'][self.item_list][2][self.item]
    #     item = self.AllowedContent(saved)
    #     collection[0] = item
    #     # Index of ItemsCollection correctly set
    #     self.assertEqual(collection[0], item)

    #     saved = self.message['body'][self.item_list][0][self.item]
    #     collection[0] = saved
    #     # Item corectly casted to self.AllowedContent
    #     self.assertEqual(type(collection[0]),self.AllowedContent)
    #     # Item content integrity
    #     self.assertEqual(collection[0][self.item_id], saved[self.item_id])
    #     # Wrong setting
    #     self.assertRaises(IndexError, collection.__setitem__, 9, saved)
    #     self.assertRaises(TypeError, collection.__setitem__, 'test', saved)

    def test_page(self):
        items = [ i[self.item] for i in self.message['body'][self.item_list] ]
        collection = self.Class(*items)
        self.assertEqual(len(collection), 3)
        for i in range(3):
            self.assertEqual(type(collection[i]), self.AllowedContent)
        page = collection.page(1,2)
        self.assertEqual(len(page), 1)
        self.assertEqual(type(page), self.Class)
        self.assertEqual(type(page[0]), self.AllowedContent)

    def test_pages(self):
        items = [ i[self.item] for i in self.message['body'][self.item_list] ]
        collection = self.Class(*items)
        self.assertEqual(len(collection), 3)
        pages = collection.pages(2)
        self.assertEqual(pages, 2)

    def test_paged(self):
        items = [ i[self.item] for i in self.message['body'][self.item_list] ]
        collection = self.Class(*items)
        self.assertEqual(len(collection), 3)
        for i in range(3):
            self.assertEqual(type(collection[i]), self.AllowedContent)
        paged = collection.paged(2)
        self.assertEqual(len(paged), 2)
        for i,l in zip(range(2), (2,1)):
            self.assertEqual(len(paged[i]), l)
            self.assertEqual(type(paged[i]), self.Class)
        for p,i in [(0,0),(0,1),(1,0)]:
            self.assertEqual(id(paged[p][i]), id(collection[(2*p)+i]))

    def test_pager(self):
        items = [ i[self.item] for i in self.message['body'][self.item_list] ]
        collection = self.Class(*items)
        self.assertEqual(len(collection), 3)
        for i in range(3):
            self.assertEqual(type(collection[i]), self.AllowedContent)
        pager = []
        for page in collection.pager(2):
            self.assertEqual(type(page), self.Class)
            self.assertEqual(type(page[0]), self.AllowedContent)
            pager.append(page)
        self.assertEqual(len(pager), 2)
        self.assertEqual(len(pager[0]), 2)
        self.assertEqual(len(pager[1]), 1)

    def test__add__(self):
        items = [ i[self.item] for i in self.message['body'][self.item_list] ]
        collection1 = self.Class(*items[:2])
        collection2 = self.Class(*items[1:3])
        collection3 = collection1 + collection2
        # Collection correctly created
        self.assertEqual(type(collection3), self.Class)
        self.assertEqual(len(collection3), 3)

