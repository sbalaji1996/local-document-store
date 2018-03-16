from imds import DocDB
from lds import DocumentDB
import timeit


if __name__ == '__main__':
    db = DocDB()
    db.add('{"year":"2017", "months": [{"m":"january"}, {"m":"february"}]}')
    db.add('{"year":"2017", "months": [{"m":"march"}, {"m":"april"}]}')
    #print(db.doc_store)
    print(db.search('{"m":"march"}'))
    start = timeit.default_timer()
    print(start)
    insert = []
    for i in range(100000):
        if i % 5 == 0:
            if i % 10 == 0:
                insert += '{\
                                "name": "bear", \
                                "classes": [{"dep": "math", "course": "54"}, {"dep": "CS", "course": "170"}], \
                                "school": {"state": "california"}\
                            }',
            else:
                insert += '{"name": "bear", "year": "junior", "school": {"state": "california"}}',
        else:
            insert += '{"name": "husky", "school": {"state": "washington"}}',
    db.add_many(insert)
    middle = timeit.default_timer()
    print(middle-start)
    #for i in db.search('{"school": {"state": "california"}, "dep": "phil"}'):
        #print(i)
    print(len(db.search('{"school": {"state": "california"}, "dep": "phil"}')))
    end = timeit.default_timer()
    print(end-middle, end-start)