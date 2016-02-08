import sys
from irsolver import irsolver

def mainn(in_file, out_file, index) :
	ids, pred = irsolver(in_file, index)
	generate_result(ids, pred, out_file)

def generate_result(ids, pred, out_file) :
	f = open(out_file, 'w')
	f.write('id,correctAnswer\n')
	for idx, p in zip(ids, pred) :
		f.write(str(idx) + ',' + p + '\n')
	f.close()

if __name__ == '__main__' :
	inp = sys.argv[1]
	out = sys.argv[2]
	index = sys.argv[3]
	mainn(inp, out, index)
