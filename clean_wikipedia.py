import re

def clean_wikipedia(in_file, out_file) :
	f = open(in_file)
	g = open(out_file, 'w')

	remove = ['-', '_', '/', '\\', '(', ')', '{', '}', '[', ']', '|', '#', '`', '<', '>', "'", '"', '@', '*', '+', '=']
	for i, line in enumerate(f) :
		line = line.decode('utf-8').split('\t')
		title = line[0]
		if re.search(r'^(.*):', title) is not None :
			continue
		if len(line) == 3 :
			text = line[2]
		else :
			text = line[1]
		text = re.sub(r'<ref(.*?)>(.*?)</ref>', r' ', text)
		text = re.sub(r'<ref(.*?)>', r' ', text)
		text = re.sub(r'\{\{(.*?)\}\}', r' ', text)
		text = re.sub(r'File:(.*?)\s', r' ', text)
		for r in remove :
			text = text.replace(r, ' ')
		text = re.sub(r'([\.\?\!,;:=+~])(\D)', r' \1 \2', text)
		text = re.sub(r'\s+', r' ', text)
		g.write(title.encode('utf-8') + '\t' + text.encode('utf-8') + '\n')
		if i % 100000 == 0 :
			print("Done %d" % i)

if __name__ == '__main__' :
	clean_wikipedia('Wikipedia_Dump/enwiki.txt', 'Wikipedia_Dump/enwiki_clean.txt')
