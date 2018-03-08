import math

from readers import read_relevance, read_queries
from search import search_query

query_document_relevance = {}
ideal_ndcg = {}

'''
DO NOT MODIFY THIS CLASS.
'''


def ideal_ndcg_queries():
    query_relevance = {}
    for relevance in read_relevance():
        query_id = relevance['query_num']
        doc_id = relevance['id']
        position = 5 - relevance['position']
        query_document_relevance[str(query_id) + "_" + str(doc_id)] = position
        if query_id in query_relevance:
            query_relevance[query_id].append(position)
        else:
            query_relevance[query_id] = [position]

    for key, value in query_relevance.items():
        sorted_relevance = sorted(query_relevance[key], reverse=True)
        count = 1
        sum = 0.0
        for each in sorted_relevance:
            sum = sum + each / math.log10(count + 1)
            count = count + 1
        ideal_ndcg[str(key)] = sum


def calculate_dcg(query, documents):
    count = 1
    sum = 0.0
    for document in documents:
        relevance =0
        key = str(query['query number']) + "_" + str(document)
        if key in query_document_relevance:
            relevance = query_document_relevance[key]
        sum = sum + relevance / math.log10(count + 1)
        count = count + 1
    return sum


if __name__ == '__main__':
    ideal_ndcg_queries()
    sum = 0.0
    all_queries = [query for query in read_queries() if query['query number'] != 0]
    for query in all_queries:
        documents = search_query(query)
        assert len(documents)==len(set(documents)), "Search results should not have duplicates:"+str(documents)
        if len(documents) > 0:
            print "Query:{} and Results:{}".format(query, documents)
            dcg = calculate_dcg(query, documents)
            idcg = ideal_ndcg[str(query['query number'])]
            ndcg = dcg / idcg
            print "dcg={}, ideal={}, ndcg={}".format(dcg, idcg, ndcg)
            sum = sum + ndcg
    print "Final ncdg for all queries is {}".format(sum / len(all_queries))
