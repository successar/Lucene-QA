Platform Used : Windows 10, 64 bit
Minimum Memory Requirements : 4GB, 8GB or above Recommended
Processor used : AMD A8 (1.65GHz) - 4 cores

Needed Open Source Programs (Detailed instructions to install them can be provided if needed):
A) Python 2.7 32-bit
B) jdk-8u65-windows-i586
C) NLTK 3.1 Library (PYTHON) - Including all Packages available in nltk.download()
D) LUCENE Version 5.4.0 (JAVA)
E) PyLucene Version 4.10.1 (PYTHON+JAVA)
F) Ant 1.9.6

Please include all LUCENE 5.4.0 JAR Files in the CLASSPATH Environment Variable

DATA SOURCES Used :
A) Wikipedia Dump (https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2) - CCA-SA 3.0 License (File Size : 11.6GB, MD5 Hash : 8bdcb0ae2fff65e052f98e7127607ea1)
B) CK-12 Books (Epub Format Downloaded - semi-automatically extracted, cleaned and parsed into topic-wise subfiles into Folder 'Data/concepts') - CC BY-NC 3.0 License
C) Grade 8 Science Textbooks (http://www.schools.utah.gov/CURR/science/OER.aspx, PDF's extracted, manually cleaned and parsed into topic-wise Subfiles into Folder 'Data/concepts') - CCA License
D) Manually authored Question Bank - By identifying common patterns/concepts of grade 8 questions in standardised tests (with help of Grade 8 Science Teachers and Students), we used crowdsourcing to develop a bank of 2,000+ question which are stored in form of statements of facts (using Sources B and C as above). This is based on psychology of development of standardised tests which form a core component when taking such tests in real life. (We didn't use any copyrighted/private/licensed material - all data came form our brains, Sources B and C and our understanding of grade 8 tests.)

Test Files Needed :
A) <data_file_path> - Specify the path to the questions file (similar to format of validation_set.tsv, including headers) eg 'data/test_set.tsv'
B) <output_file_path> - Specify the path where the answers file should be generated (similar to format of sample submissiob.csv) eg 'data/output.csv'

#########################################

In command line : go to folder 'nlp'
All Command Line actions below are to be performed in this folder.

Store questions file 'test_set.tsv' in folder 'Data'

#########################################

Extract and clean Wikipedia Dump

1) Download Latest Wikipedia Dump from https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
2) Extract the file enwiki-latest-pages-articles.xml in folder labeled 'Wikipedia_Dump'
3) Run Lucene Task from Command Line : ant run-task -Dtask.alg=extractWikipedia.alg
4) Run from command line : python clean_wikipedia.py

There should be two files (in 'Wikipedia_Dump' folder) : enwiki.txt | enwiki_clean.txt
(This step might take some time)

In following : <path_to_"enwiki_clean.txt"_file> = Wikipedia_Dump/enwiki_clean.txt

#########################################

Create Wikipedia LUCENE Indices

1) Run from Command Line : python wikipedia_indexer.py index_clean/ <path_to_"enwiki_clean.txt"_file>

This should create one new folder (in 'nlp' Directory) : index_clean/
(We have already included the created index files)
(These index files may take some time to generate)

#########################################

Extract Relevant pages from testing data

1) Run from Command Line : python get_wiki_pages.py <data_file_path> <path_to_"enwiki_clean.txt"_file> index_clean/

#########################################

Create new Indices for Question-Answering

1) Run from Command Line : python sentence_indexer.py index_sent/
2) Run from Commans Line : python statements_indexer.py index_sent/

This should create a new folders (in 'nlp' Directory) : index_sent/ 

#########################################

Actual QA Using Previously created indices

1) Run from Command Line : python sarthak.py <data_file_path> <output_file_path> index_sent/

#########################################

The predictions should be available at <output_file_path>
