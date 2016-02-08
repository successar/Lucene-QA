import sys, lucene, re

from java.io import File
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import IndexReader

def get_wiki_nums(data_file, wikipedia_index) :
	lucene.initVM()
	reader = IndexReader.open(SimpleFSDirectory(File(wikipedia_index)))
	searcher = IndexSearcher(reader)
	id_file = open(data_file + '.docid')
	num_file = open(data_file + '.nums', 'w')
	what = []
	for line in id_file :
		line = line.strip()
		if len(line) == 0 :
			continue
		line = line.split('\t')
		if len(line) == 2 and int(line[1]) not in [-1, 0, 1, 2, 3]:
			what.append(int(line[1]))

	what = list(set(what))

	for item in what :
		num_file.write(str(item) + '\t' + searcher.doc(item).get("num").encode('utf-8') + '\n')



	