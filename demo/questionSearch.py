from collections import OrderedDict
from SPARQLWrapper import SPARQLWrapper, JSON


class sparqlConnect:
    def __init__(self, url="http://localhost:3030/virus/query"):
        self.sparqlConnect = SPARQLWrapper(url)   # server connect

    def get_sparql_result(self, query):
        self.sparqlConnect.setQuery(query)
        self.sparqlConnect.setReturnFormat(JSON)
        return self.sparqlConnect.query().convert()

    def parse_result(self, query_result):   # 解析结果json
        try:
            query_head = query_result['head']['vars']
            query_results = list()
            for r in query_result['results']['bindings']:
                temp_dict = OrderedDict()
                for h in query_head:
                    temp_dict[h] = r[h]['value']
                query_results.append(temp_dict)
            return query_head, query_results
        except KeyError:
            return None, query_result['boolean']

    def get_sparql_result_value(self, query_result):
        query_head, query_result = self.parse_result(query_result)
        if query_head is None:
            return query_result
        else:
            values = list()
            for qr in query_result:
                for _, value in qr.items():
                    if 'http' in value:
                        continue
                    if len(value) < 1:
                        continue
                    if self.count_alpha(value):
                        continue
                    values.append(value)
            return values

    def count_alpha(self, string):
        cnt = 0
        for i in string.lower():
            if i in ['a', 'e', 's', 'i', 'p']:
                cnt += 1
        if cnt > len(string)/5:
            return True
        return False
