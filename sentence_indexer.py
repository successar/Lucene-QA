import sys, re, lucene
from nltk.tokenize import sent_tokenize

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.util import CharArraySet
from org.apache.lucene.document import Document, Field
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

from java.util import HashSet, Arrays
from utility import stopwords

remove = ['-', '_', '/', '\\', '(', ')', '{', '}', '[', ']', '|', '#', '`', '<', '>', "'", '"', '@', '*', '+', '=', '^', '~', '&']

def get_data_from_text(text) :
	text = text
	for r in remove :
		text = text.replace(r, ' ')
	text = re.sub(r'[ \r\f](\d)\.(\d)\.(\d)[ \r\f]', r' \1\2\3 ', text)
	text = re.sub(r'([\.\?\!,;])(\D)', r' \1 \2', text)
	text = re.sub(r'\s+', r' ', text)
	return text

def get_data_from_file(filen) :
	f = open(filen)
	text = f.read().decode('utf-8')
	return get_data_from_text(text)


def create_index(storage, paths) :
	lucene.initVM()
	indexDir = SimpleFSDirectory(File(storage))
	stops = CharArraySet(Version.LUCENE_4_10_1, 0, True)
	for s in stopwords :
		stops.add(s)
	analyzer = StandardAnalyzer(Version.LUCENE_4_10_1, stops)
	writerConfig = IndexWriterConfig(Version.LUCENE_4_10_1, analyzer)
	writer = IndexWriter(indexDir, writerConfig)

	print "%d docs in index" % writer.numDocs()
	print "Reading Documents"

	import os
	for path in paths :
		for filen in os.listdir(path) :
			text = sent_tokenize(get_data_from_file(path + filen))
			total_sent = len(text)
			for i in range(0, total_sent, 3) :
				doc = Document()
				a = i-5 if i-5 > 0 else 0
				sentence = ' '.join(text[a:i+5])
				doc.add(Field("text", sentence, Field.Store.YES, Field.Index.ANALYZED))
				writer.addDocument(doc)
			print("Done %s" % (path+filen))
			print "Indexed (%d docs in index)" % (writer.numDocs())
	print "Closing index of %d docs..." % writer.numDocs()
	writer.close()

if __name__ == "__main__" :
	paths = ['Data/concepts/', 'Data/keywords_wiki/' , 'Data/extracted_wiki_pages/']
	import sys
	create_index(sys.argv[1], paths)