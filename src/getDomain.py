#coding=utf8


domains= set()
for l in open('../data/hoststools.txt').readlines():
	if l [0] != '#':
		domains.add(l.strip().split(' ')[-1])

fout = open('../data/domains.txt','w')
for d in domains:
	fout.write(d+'\n')
fout.close()