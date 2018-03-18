import json


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

    def update(self, match, updated_val):
        match_json = self.__convert_str_json(match)
        update_json = self.__convert_str_json(updated_val)
        match_base_pairs = set(self.__key_val_extract(match_json))
        for i, item in enumerate(self._documents):
            pairs, raw = item
            if match_base_pairs <= pairs:
                updated_doc = {**raw, **update_json}
                updated_doc_base_pairs = set(self.__key_val_extract(updated_doc))
                self._documents[i] = (updated_doc_base_pairs, updated_doc)
        return True

    def __convert_str_json(self, item):
        if isinstance(item, str):
            return json.loads(item)
        return item

    def __key_val_extract(self, doc):
        extracted_pairs = []
        for key, value in doc.items():
            if isinstance(value, dict):
                extracted_pairs += (key, 'nested_json'),
                extracted_pairs.extend(self.__key_val_extract(value))
            elif isinstance(value, list):
                extracted_pairs += (key, 'nested_list'),
                extracted_pairs.extend(self.__list_extract(value))
            else:
                extracted_pairs += (key, value),
        return extracted_pairs

    def __list_extract(self, doc_list):
        extracted_pairs = []
        for item in doc_list:
            extracted_pairs.extend(self.__key_val_extract(item))
        return extracted_pairs
