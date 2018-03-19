import json
import itertools


class DocStore:
    def __init__(self):
        self._documents = []

    def add(self, doc):
        doc_json = self.__convert_str_json(doc)
        document_base_pairs = set(self.__key_val_extract(doc_json))
        self._documents += (document_base_pairs, doc_json),

    def add_many(self, docs):
        for doc in docs:
            self.add(doc)

    def search(self, query):
        query_json = self.__convert_str_json(query)
        query_base_pairs = set(self.__key_val_extract(query_json))
        return [raw for pairs, raw in self._documents if query_base_pairs <= pairs]

    def update(self, match, new, exact=False):
        match_json = self.__convert_str_json(match)
        new_json = self.__convert_str_json(new)

        if exact:
            if len(match_json) != 1 or len(new_json) != 1:
                return
            match_pair = list(match_json.items())[0]
            new_pair = list(new_json.items())[0]

        match_base_pairs = set(self.__key_val_extract(match_json))
        for i, item in enumerate(self._documents):
            pairs, raw = item
            if match_base_pairs <= pairs:
                if exact:
                    updated_doc = self.__update_exact_helper(raw, match_pair, new_pair)
                else:
                    updated_doc = {**raw, **new_json}
                updated_doc_base_pairs = set(self.__key_val_extract(updated_doc))
                self._documents[i] = (updated_doc_base_pairs, updated_doc)

    def __convert_str_json(self, item):
        if isinstance(item, str):
            return json.loads(item)
        return item

    def __update_exact_helper(self, prev, match, new):
        updated = prev.copy()
        new_key, new_val = new
        for key, value in prev.items():
            if isinstance(value, dict):
                updated[key] = self.__update_exact_helper(value, match, new)
            elif isinstance(value, list):
                updated[key] = [self.__update_exact_helper(item, match, new) for item in value]
            elif (key, value) == match and key == new_key:
                updated[key] = new_val
        return updated

    def __key_val_extract(self, doc):
        extracted_pairs = []
        for key, value in doc.items():
            if isinstance(value, dict):
                extracted_pairs += (key, 'nested_json'),
                extracted_pairs.extend(self.__key_val_extract(value))
            elif isinstance(value, list):
                extracted_pairs += (key, 'nested_list'),
                pairs_from_list = [self.__key_val_extract(item) for item in value]
                extracted_pairs.extend(list(itertools.chain(*pairs_from_list)))
            else:
                extracted_pairs += (key, value),
        return extracted_pairs
