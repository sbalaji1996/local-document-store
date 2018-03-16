import json
from collections import defaultdict


class DocumentDB:
    def __init__(self):
        self.documents = []

    def add(self, doc):
        self.documents += defaultdict(None, json.loads(doc)),

    def add_many(self, docs):
        for doc in docs:
            self.add(doc)

    def search(self, query):
        q_items = json.loads(query).items()
        return [item for item in self.documents if q_items <= item.items()]
