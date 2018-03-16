import json
import zlib


class DocDB:
    def __init__(self, compress_docs=False):
        self.doc_store = []
        self.compress_docs = compress_docs

    def add(self, document):
        compressed_doc = zlib.compress(document.encode('utf-8')) \
                            if self.compress_docs else document
        #document_base_dict = {key: value for key, value in
                              #self.__key_val_extract(json.loads(document))}
        document_base_dict = set(self.__key_val_extract(json.loads(document)))
        #print(document_base_dict)
        self.doc_store += (document_base_dict, compressed_doc),

    def add_many(self, documents):
        for document in documents:
            self.add(document)

    def search(self, query):
        #query_dict = {key: value for key, value in
                      #self.__key_val_extract(json.loads(query))}
        #print(query_dict)
        query_dict = set(self.__key_val_extract(json.loads(query)))
        #print(query_dict)
        #print(self.doc_store[0][0])
        if self.compress_docs:
            # return [zlib.decompress(raw_doc) for doc, raw_doc in self.doc_store
            #         if query_dict.items() <= doc.items()]
            return [zlib.decompress(raw_doc) for doc, raw_doc in self.doc_store
                    if query_dict <= doc]
        else:
            # return [raw_doc for doc, raw_doc in self.doc_store
            #         if query_dict.items() <= doc.items()]
            return [raw_doc for doc, raw_doc in self.doc_store
                    if query_dict <= doc]

    # def __key_val_extract(self, doc_dict):
    #     for key, value in doc_dict.items():
    #         if not isinstance(value, dict):
    #             yield (key, value)
    #         else:
    #             yield (key, 'nested_json')  # to enforce an exact match
    #             for val in self.__key_val_extract(value):
    #                 yield val

    def __key_val_extract(self, doc_dict):
        extracted_pairs = []
        for key, value in doc_dict.items():
            if isinstance(value, dict):
                extracted_pairs += (key, 'nested_json'),
                extracted_pairs.extend(self.__key_val_extract(value))
            elif isinstance(value, list):
                extracted_pairs += (key, 'nested_list'),
                for pair in self.__key_val_extract_list(value):
                    #print(pair[0])
                    extracted_pairs += (pair[0], pair[1]),
                    #print(extracted_pairs)
                # base_list = []
                # for pair in self.__key_val_extract_list(value):
                #     base_list += pair,
                # extracted_pairs += (key, base_list),
            else:
                extracted_pairs += (key, value),
        return extracted_pairs

    def __key_val_extract_list(self, doc_list):
        extracted_pairs = []
        for item in doc_list:
            extracted_pairs.extend(self.__key_val_extract(item))
        return extracted_pairs