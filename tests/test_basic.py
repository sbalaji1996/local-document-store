from .context import imds
import unittest
import json


class BasicTestSuite(unittest.TestCase):
    def test_basic(self):
        db = imds.DocStore()
        first = '{"year":"2017", "months": [{"m":"january"}, {"m":"february"}]}'
        second = '{"year":"2017", "months": [{"m":"march"}, {"m":"april"}]}'
        db.add(first)
        db.add(second)

        assert db.search('{"m":"march"}') == [json.loads(second)]
        assert db.search('{"m":"may"}') == []

        third = '{"year":"2017", "months": [{"m":"may"}, {"m":"april"}]}'
        db.update('{"m":"march"}', '{"months": [{"m":"may"}, {"m":"april"}]}')

        assert db.search('{"m":"march"}') == []
        assert db.search('{"m":"may"}') == [json.loads(third)]

    def test_basic_update(self):
        db = imds.DocStore()
        first = '{"year":"2017", "months": [{"m":"january"}, {"m":"february"}]}'
        second = '{"year":"2017", "months": [{"m":"march"}, {"m":"april"}]}'
        db.add(first)
        db.add(second)

        assert db.search('{"m":"march"}') == [json.loads(second)]
        assert db.search('{"m":"may"}') == []

        third = '{"year":"2017", "months": [{"m":"may"}, {"m":"may"}]}'
        db.update_slow('{"m":"march"}', 'm', 'may')
        assert db.search('{"m":"march"}') == []
        assert db.search('{"m":"may"}') == [json.loads(third)]


if __name__ == '__main__':
    unittest.main()
