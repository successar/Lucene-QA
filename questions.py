def get_input_data(in_file) :
	g = open(in_file)
	idx = []
	ques = []
	ans = []
	ids = 2

	for line in g :
		line = line.decode('utf-8').strip().split('\t')
		idx.append(line[0])
		ques.append(line[1])
		a = []
		for i in range(ids, ids + 4) :
			a.append(line[i])
		ans.append(a)

	idx, ques, ans = idx[1:], ques[1:], ans[1:]

	return idx, ques, ans	