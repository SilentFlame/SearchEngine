'''
Author: Vinay Singh
Topis: Information Retrieval
About: Implementing the creation of indexes from the data file
'''

#!/usr/bin/env python

# The required libraries
import sys
import re
from nltk.stem import PorterStemmer 
from collections import defaultdict
from array import array
import gc
import json
import math
import operator
from collections import OrderedDict

# importing the steer
porter=PorterStemmer()

class CreateIndex():
    
    def __init__(self):
        self.index = defaultdict(list)
        self.tf_idf_index = defaultdict(list)
        
    
    # tokenzation needed to call for he query when needed
    def tokenize(self, text):
        return text.split(" ")

    def remove_not_indexed_toknes(self, tokens):
        return [token for token in tokens if token in self.index]
    
    # getting the stopwords
    def getStopwords(self):
        '''get stopwords from the stopwords file'''
        # you need this file in your directory 
        f=open('./resources/stopwords.txt', 'r')
        stopwords=[line.rstrip() for line in f]
        sw=dict.fromkeys(stopwords)
        f.close()
    
        return sw
    
    # loading the queies
    def loadQueries(self):
        return json.load(open('./resources/cran.qry.json'))
    
    
    # getting tokens and stem terms from the text given
    def getTerms(self, line):
        # given a stream of text, get the terms from the text
        line=line.lower()
        line=re.sub(r'[^a-z0-9 ]',' ',line) #put spaces instead of non-alphanumeric characters
        line=line.split()
        # from the list of stowords
        sw = self.getStopwords()
        line=[x for x in line if x not in sw ]  #eliminate the stopwords
        line=[ porter.stem(word) for word in line]
        return line

    # total number of docs containing a term
    def doc_containing(self, word):
        total_docs = 0
        for p in self.index[word]:
            total_docs += 1
        return total_docs
    
    # calculating the idf score
    def idf(self, word):
        return math.log(len(self.index)/(1+self.doc_containing(word)))
    
    # calculating the tf score
    def tf(self, word, doc):
        word_count = 0
        for ind in xrange(0, len(doc)):
            if doc[ind] == word:
                word_count+=1

        # print("doc: word_count: {}, len_doc: {}".format(word_count, len(doc)))
        tf_value = round((float(word_count)/len(doc)), 5)
        # print("TF: word {}, score: {}".format(word, tf_value))
        return tf_value
   
   
    # calculating the tf-idf scores of a term
    def scoreTfIdf(self, term, doc):
        tf_score = self.tf(term, doc)
        idf_score = self.idf(term)
        
        return tf_score*idf_score
    
    
    # parsing the json data doc by doc
    def parseCollection(self, fileData):
        # returning the ID, author, bibliography, body and title of the doc
        d = {}
        d['id'] = fileData['id']
        d['author'] = fileData['author']
        d['bibliography'] = fileData['bibliography']
        d['body'] = fileData['body']
        d['title'] = fileData['title']
    
        return d
    
    # writing tf-idf indexes to a file
    def writeTfIdfToFile(self):
        # f=open('tf-idfIndexFile.txt', 'w')
        
        for term in sorted(self.index.iterkeys()):
            postinglist=[]
            for p in self.tf_idf_index[term]:
                docID=p[0]
                score=p[1]
                # print len(positions)
                # print("term: {}, docID: {}, score: {}".format(term, docID, score))
                
        #         postinglist.append(''.join((str(docID),':', ','.join(str(score)))))
        #     print >> f, ''.join((term,'|',';'.join(postinglist)))
            
        # f.close()
    
    # the process to get the best Ids
    def bestDocIds(self, indexed_tokens):
        docs_score = {}
        for term in indexed_tokens:
            for p in self.tf_idf_index[term]:
                # print type(p[0]), type(p[1])
                if p[0] in docs_score.keys():
                    docs_score[p[0]] += float(p[1])
                else:
                    docs_score[p[0]] = float(p[1])
                    # print docs_score[p[0]]
        
        result_dict = OrderedDict(sorted(docs_score.items(), key=lambda x: x[1]))
        
        # print .keys()
        return docs_score.keys()
    
    
    # the final process to find the best doc Id's
    def resultDocIds(self, query):
        # tokens = self.tokenize(str(query))
        tokens = self.getTerms(str(query))
        indexed_tokens = self.remove_not_indexed_toknes(tokens)
        
        if len(indexed_tokens) == 0:
            return []
        elif len(indexed_tokens) == 1:
            return self.tf_idf_index[indexed_tokens[0]][0]
        else:
            return self.bestDocIds(indexed_tokens)
    
    
    # the search query function
    # def search_query(self, all_queries):
    #     for query in all_queries():
    #         results = self.resultDocIds(query)
    #         print "Query:{} and Results:{}".format(query, results)
    
    
    # making a new index with the tf-Idf score of all the terms
    def createIndexTfIdf(self):
        # reading the json fie again
        data = json.load(open('./resources/cranfield_data.json'))
        
        # dict. of all the pages(docs) in the json file
        pagedict={}
        for rows in xrange(0, len(data)):
            
            # parsing the data into mentioned feilds.
            pagedict=self.parseCollection(data[rows])
            
            # data from the file
            lines='\n'.join((pagedict['author'], pagedict['bibliography'], pagedict['body'], pagedict['title'] ))
            pageid = int(pagedict['id'])
            
            # tokenizing and stemming the data contents from the docs
            terms=self.getTerms(lines)
            
            #build the index for the current page(doc)
            termdictPage={}
            for position, term in enumerate(terms):
                # score of tf-idf
                score = self.scoreTfIdf(term, terms)
                
                # need to see here the case of except
                try:
                    termdictPage[term][1].append(score)
                except:
                    termdictPage[term]=[pageid, score]
                
            # merge the current page index with the main index
            for termpage, postingpage in termdictPage.iteritems():
                self.tf_idf_index[termpage].append(postingpage)
        # to see how our tf-idf are structured
        # self.writeTfIdfToFile()
        
    
    
    # defining the index creating function
    def createIndex(self):
        # reading the json file
        data = json.load(open('./resources/cranfield_data.json'))
        
        # dict. of all the pages(docs) in the json file
        pagedict={}
        # iterating over all the doc data
        for rows in xrange(0, len(data)):
            # parsing the data into mentioned feilds.
            pagedict=self.parseCollection(data[rows])
            
            # data from the file
            lines='\n'.join((pagedict['author'], pagedict['bibliography'], pagedict['body'], pagedict['title'] ))
            pageid = int(pagedict['id'])
            # tokenizing and stemming the data contents from the docs
            terms=self.getTerms(lines)
            
            #build the index for the current page(doc)
            termdictPage={}
            for position, term in enumerate(terms):
                # need to see here the case of except
                try:
                    termdictPage[term][1].append(position)
                except:
                    termdictPage[term]=[pageid, array('I',[position])]
                
            # merge the current page index with the main index
            for termpage, postingpage in termdictPage.iteritems():
                self.index[termpage].append(postingpage)
        
        # creating an index with tf-idf scores
        self.createIndexTfIdf()
        
        # Moving to the processing of the queries
        # all_queries = self.loadQueries()
        # for query in all_queries:
        #     results = self.resultDocIds(query)
        #     print "Query:{} and Results:{}".format(query, results)
        #     break

        # we can write this index and all to a file and see how our index was made
        # self.writeIndexToFile()
        
    
if __name__ == "__main__":
    I = CreateIndex()
    I.createIndex()