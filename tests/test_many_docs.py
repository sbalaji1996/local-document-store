from .context import imds
import unittest
import json


class BasicTestSuite(unittest.TestCase):
    def construct_db(self):
        db = imds.DocStore()

        insert = []
        for i in range(1000):
            if i % 5 == 0:
                if i % 10 == 0:
                    insert += '{\
                                    "name": "oski", \
                                    "classes": [{"dep": "math", "course": "54"}, {"dep": "cs", "course": "170"}], \
                                    "school": {"state": "california"}\
                                }',
                else:
                    insert += '{\
                                    "name": "oski jr", \
                                    "classes": [{"dep": "phil", "course": "12"}, {"dep": "psych", "course": "127"}], \
                                    "school": {"state": "california"}\
                                }',
            else:
                insert += '{\
                                "name": "harry", \
                                "classes": [{"dep": "bio", "course": "1a"}, {"dep": "chem", "course": "1b"}], \
                                "school": {"state": "washington"}\
                            }',
        db.add_many(insert)
        return db

    def test_large_matches(self):
        db = self.construct_db()

        assert len(db.search('{}')) == 1000
        assert len(db.search('{"dep": "math"}')) == 100
        assert len(db.search('{"classes": [{"dep": "math"}, {"dep": "cs"}]}')) == 100
        assert len(db.search('{"dep": "math", "course": "54"}')) == 100
        assert len(db.search('{"classes": [{"dep": "math", "course": "54"}, {"dep": "cs"}]}')) == 100

        assert len(db.search('{"name": "joe"}')) == 0
        assert len(db.search('{"school": "california"}')) == 0
        assert len(db.search('{"classes": [{"dep": "math"}, {"dep": "psych"}]}')) == 0

    def test_large_updates(self):
        db = self.construct_db()

        assert len(db.search('{}')) == 1000
        assert len(db.search('{"dep": "bio"}')) == 800
        assert len(db.search('{"name": "harry"}')) == 800

        db.update('{"dep": "bio"}', '{"dep": "biology"}', exact=True)

        assert len(db.search('{"dep": "bio"}')) == 0
        assert len(db.search('{"dep": "biology"}')) == 800

        db.update('{"dep": "biology"}', '{"classes": "withdrawn"}')

        assert len(db.search('{"dep": "biology"}')) == 0
        assert len(db.search('{"name": "harry"}')) == 800
        assert len(db.search('{"name": "harry", "dep": "chem"}')) == 0