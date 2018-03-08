# SearchEngine #
**About:**  Implementation of a inverse index based query search engine 


### Libraries required ###
- import sys
- re
- nltk 
- collections
- json
- math
- operator

-----

### Preprocessing ###
- Parsing the json data to load data to respective feilds.
- Concatination of texts from all the fields in the data of a file.
- Replacing the non-alphabetic charecters with spaces.
- Removing the stopwords from the text data.
- Stemming of the words (used Porter stemmer from nltk.stem).

------

### Creating Index ###
- Created two types of index
- One with Word and docId of docs that contain it along with it's frequncy in that doc
- Other with Word and docId of docs that contain that word with the tf-idf score of the word.

`can uncomment some of the parts in the code to write these indexes in files to look it yourself.`

----
### Calculating Scores ###
- For each word we calculate the tf-idf score.
- For more insights regarding the formulation of tf and idf independently please visit  [here](https://en.wikipedia.org/wiki/Tf%E2%80%93idf).

----

### Query processing ###
- loadQueries is the function that loads the queries already present in the file inside `/resources/`.
- query is tokenized and stemmed as we did the document texts while preparing the indexes.
- tokens not present in the indexing are dropped from the query token, `see line #149 of createIndex.py`.

---

### Results ###
- Our system returns a list of docIds in the order of `higher to lower` relevance.
- The docIds at begining are more relevent to our query as compared to the later once.
- These are compared on the tf-idf scores computed for all the words of the query across all the documents.
- Systems nDCG (relevance) score is ~0.6 which is a good score for as basic and naive method we have implemented here.
---
#### Future Work ####
- can use semantics to get more favourable words related to a word in the query.
- Specific to feild query cases to be handled.

-----
##### Discussions #####
Join [![Join the chat at https://gitter.im/IndexingDiscussion/Lobby](https://badges.gitter.im/IndexingDiscussion/Lobby.svg)](https://gitter.im/IndexingDiscussion/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) for discussions and doubts regarding the workflow of the system.

