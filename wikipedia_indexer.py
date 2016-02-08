import sys
import lucene
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.util import CharArraySet
from org.apache.lucene.document import Document, Field
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
from utility import stopwords

def wikipedia_indexer(storage, wikipedia_file) :
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

	f = open(wikipedia_file)

	for i, line in enumerate(f) :
		text = line.strip().decode('utf-8').split('\t')
		title = text[0]
		if 'disambigu' in text[0] or len(text) < 2:
			continue
		text = text[1]
		doc = Document()
		doc.add(Field("num", str(i), Field.Store.YES, Field.Index.NO))
		doc.add(Field("title", title, Field.Store.YES, Field.Index.ANALYZED))
		doc.add(Field("text", text, Field.Store.NO, Field.Index.ANALYZED))
		writer.addDocument(doc)
		if writer.numDocs() % 1000 == 0 :
			print "Indexed (%d docs in index) Last %d" % (writer.numDocs(), i)
		
	print "Closing index of %d docs..." % writer.numDocs()
	writer.close()	

if __name__ == '__main__' :
	wikipedia_indexer(sys.argv[1], sys.argv[2])
