from get_wiki_docids import get_wiki_docids
from get_wiki_nums import get_wiki_nums

def get_wiki_pages(data_file, wikipedia_file, wikipedia_index) :
	get_wiki_docids(data_file, wikipedia_index)
	get_wiki_nums(data_file, wikipedia_index)

	num_file = open(data_file + '.nums')
	output_folder = 'Data/extracted_wiki_pages'
	what = []

	for line in num_file :
		line = line.strip().split('\t')
		if len(line) == 0 :
			continue
		what.append(int(line[1]))

	what = list(set(what))
	what.sort()
	print(len(what), "    extracting relevant wiki files ................")

	j = 0
	g = open(wikipedia_file)
	for i, line in enumerate(g) :
		if i == what[j] :
			j += 1
			if j == len(what) :
				break
			filen = open(output_folder + '/' + str(i) + '.txt', 'w')
			filen.write(line.decode('utf-8').encode('utf-8') + '\n')
			filen.close()
			if j % 1000 == 0 :
				print(j)

if __name__ == '__main__' :
	import sys
	get_wiki_pages(sys.argv[1], sys.argv[2], sys.argv[3])







