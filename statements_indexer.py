import sys, re
import lucene

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.util import CharArraySet
from org.apache.lucene.document import Document, Field
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
from utility import stopwords

lucene.initVM()
remove = ['-', '_', '/', '\\', '(', ')', '{', '}', '[', ']', '|', '#', '`', '<', '>', "'", '"', '@', '*', '+', '=', '^', '~', '&']
total_rem = remove

def get_data_from_text(text) :
	text = text
	for r in total_rem :
		text = text.replace(r, ' ')
	text = re.sub(r'[ \r\f](\d)\.(\d)\.(\d)[ \r\f]', r' \1\2\3 ', text)
	text = re.sub(r'([\.\?\!,;])(\D)', r' \1 \2', text)
	text = re.sub(r'\s+', r' ', text)
	return text

def create_index(index) :
	indexDir = SimpleFSDirectory(File(index))
	stops = CharArraySet(Version.LUCENE_4_10_1, 0, True)
	for s in stopwords :
		stops.add(s)
	analyzer = StandardAnalyzer(Version.LUCENE_4_10_1, stops)
	writerConfig = IndexWriterConfig(Version.LUCENE_4_10_1, analyzer)
	writer = IndexWriter(indexDir, writerConfig)

	print "%d docs in index" % writer.numDocs()
	print "Reading Documents"

	f = open('f:/nlp/data/questions/combine.txt')
	for line in f :
		line = get_data_from_text(line.decode('utf-8'))
		doc = Document()
		field = Field("text", line, Field.Store.YES, Field.Index.ANALYZED)
		field.setBoost(2.0)
		doc.add(field)
		writer.addDocument(doc)
	
	print "Indexed (%d docs in index)" % (writer.numDocs())
	print "Closing index of %d docs..." % writer.numDocs()
	writer.close()

if __name__ == "__main__" :
	import sys
	create_index(sys.argv[1])