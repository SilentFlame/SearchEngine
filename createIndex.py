# Author: Vinay Kumar Singh

#!/usr/bin/env python

import json
from nltk.stem import PorterStemmer 
from collections import defaultdict
from array import array
import re
import sys

porter=PorterStemmer()

class CreateIndex:

    def __init__(self):
        self.index=defaultdict(list)    #the inverted index

    
    def getStopwords(self):
        '''get stopwords from the stopwords file'''
        f=open('stopwords.txt', 'r')
        stopwords=[line.rstrip() for line in f]
        sw=dict.fromkeys(stopwords)
        f.close()

        return sw
        

    def getTerms(self, line):
        '''given a stream of text, get the terms from the text'''
        line=line.lower()
        line=re.sub(r'[^a-z0-9 ]',' ',line) #put spaces instead of non-alphanumeric characters
        line=line.split()
        sw = self.getStopwords()
        line=[x for x in line if x not in sw ]  #eliminate the stopwords
        line=[ porter.stem(word) for word in line]
        return line


    def parseCollection(self, fileData):
        ''' returns the id, title and text of the next page in the collection '''
        d = {}
        d['id'] = fileData['id']
        d['title'] = fileData['title']
        d['body'] = fileData['body']
        d['author'] = fileData['author']
        d['bibliography'] = fileData['bibliography']

        return d


    def writeIndexToFile(self):
        '''write the inverted index to the file'''
        f=open('IndexFileToWrite', 'w')
        for term in self.index.iterkeys():
            postinglist=[]
            for p in self.index[term]:
                docID=p[0]
                positions=p[1]
                postinglist.append(':'.join([str(docID) ,','.join(map(str,positions))]))
            print >> f, ''.join((term,'|',';'.join(postinglist)))
            
        f.close()
        

    def createIndex(self):
        '''main of the program, creates the index'''
        data = json.load(open('JSON file to read'))
                
        pagedict={}
        for rows in xrange(0, len(data)):
            pagedict=self.parseCollection(data[rows])
                           
            lines='\n'.join((pagedict['title'],pagedict['author'], pagedict['body'], pagedict['bibliography']))
            pageid=int(pagedict['id'])
            terms=self.getTerms(lines)
            
            #build the index for the current page
            termdictPage={}
            for position, term in enumerate(terms):
                try:
                    termdictPage[term][1].append(position)
                except:
                    termdictPage[term]=[pageid, array('I',[position])]
            
            #merge the current page index with the main index
            for termpage, postingpage in termdictPage.iteritems():
                self.index[termpage].append(postingpage)

            
        self.writeIndexToFile()
        
    
if __name__=="__main__":
    c=CreateIndex()
    c.createIndex()
    

