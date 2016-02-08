import sys, re, lucene
 
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.util import CharArraySet
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import IndexReader
from org.apache.lucene.queryparser.classic import QueryParser

from utility import stopwords

remove = ['-', '_', '/', '\\', '(', ')', '{', '}', '[', ']', '|', '#', '`', '<', '>', "'", '"', '@', '*', '+', '=', ':', '~']
chars = ['+','-','&&', '||', '!', '(',')','{','}','[', ']', '^', '"',"'" ,'~','*','?',',' ,':' ,'\\' ,'/']

total_rem = remove + chars

def clean_text(text) :
	for r in total_rem :
		text = text.replace(r, ' ')
	text = re.sub(r'[ \r\f](\d)\.(\d)\.(\d)[ \r\f]', r' \1\2\3 ', text)
	text = re.sub(r'([\.\?\!,;])(\D)', r' \1 \2', text)
	text = re.sub(r'\s+', r' ', text)
	return text

def query(phrase, analyzer, searcher, id_file):
	query = QueryParser(Version.LUCENE_4_10_1, "text", analyzer).parse(phrase)
	MAX = 7
	hits = searcher.search(query, MAX)
	docs = hits.scoreDocs
	for hit in docs :
		id_file.write(str(hit.score) + '\t' + str(hit.doc) + '\n')
	id_file.write('\n')

def generate_docids(data, data_file, analyzer, searcher) :
	idx, ques, ans = data

	id_file = open(data_file + '.docid', 'w')

	for idq, q, a in zip(idx, ques, ans) :
		q = clean_text(q)
		id_file.write(str(idq) + '\t-1\n')
		query(q, analyzer, searcher, id_file)
		for i, ai in enumerate(a):
			id_file.write(str(idq) + '\t' + str(i) + '\n')
			ai = clean_text(ai)
			stmt = '+(' + q + ') +(' + ai + ')'
			query(stmt, analyzer, searcher, id_file)


def get_wiki_docids(data_file, wikipedia_index) :
	from questions import get_input_data
	data = get_input_data(data_file)

	lucene.initVM()
	stops = CharArraySet(Version.LUCENE_4_10_1, 0, True)
	for s in stopwords :
		stops.add(s)
	analyzer = StandardAnalyzer(Version.LUCENE_4_10_1, stops)
	reader = IndexReader.open(SimpleFSDirectory(File(wikipedia_index)))
	searcher = IndexSearcher(reader)

	generate_docids(data, data_file, analyzer, searcher)
	


	

	
