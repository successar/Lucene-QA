import sys, re
import lucene

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.util import CharArraySet
from org.apache.lucene.document import Document, Field
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import IndexReader
from org.apache.lucene.queryparser.classic import QueryParser
from utility import stopwords

remove = ['-', '_', '/', '\\', '(', ')', '{', '}', '[', ']', '|', '#', '`', '<', '>', "'", '"', '@', '*', '+', '=', '^']
chars = [u'+',u'-',u'&&', u'||', u'!', u'(',')','{','}','[', ']', '^', '"',"'" ,u'~','*','?',',' ,':' ,'\\' ,'/']
total_rem = remove + chars

def irsolver(data_file, index) :
	from questions import get_input_data
	lucene.initVM()
	stops = CharArraySet(Version.LUCENE_4_10_1, 0, True)
	for s in stopwords :
		stops.add(s)
	analyzer = StandardAnalyzer(Version.LUCENE_4_10_1, stops)
	reader = IndexReader.open(SimpleFSDirectory(File(index)))
	searcher = IndexSearcher(reader)
	pred = []
	mapp = { 1 : 'A', 2 : 'B', 3 : 'C', 4 : 'D'}

	idx, ques, ans = get_input_data(data_file)
	for acm, (idq, q, a) in enumerate(zip(idx, ques, ans)) :
		max_score = -1000000
		best_ans = 'A'
		for i, ai in enumerate(a):
			sc = query(q, ai, analyzer, searcher)
			print(acm, i, sc)
			if sc > max_score :
				max_score = sc
				best_ans = mapp[i+1]
		pred.append(best_ans)

	return idx, pred


def get_data_from_text(text) :
	text = text
	for r in total_rem :
		text = text.replace(r, ' ')
	text = re.sub(r'\s+', r' ', text)
	text = re.sub(r'[ \r\f](\d)\.(\d)\.(\d)[ \r\f]', r' \1\2\3 ', text)
	text = re.sub(r'([\.\?\!,;=~])(\D)', r' \1 \2', text)
	return text

def query(q, a, analyzer, searcher) :
	qs = get_data_from_text(q)
	ass = get_data_from_text(a)
	phrase = '+(' + qs + ')' + ' +(' + ass + ')'
	query = QueryParser(Version.LUCENE_4_10_1, "text", analyzer).parse(phrase)
	MAX = 4
	hits = searcher.search(query, MAX)
	print(phrase, hits.totalHits)
	score = 0.0
	for i, hit in enumerate(hits.scoreDocs):
	 	score += hit.score
	return score
