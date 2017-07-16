#encoding:utf-8
import linecache

months = ['11','12','1','3','4','5','6']
all = []

for month in months :
	f = open(month+'月.txt')
	lines = f.readlines() 
	for line in lines :
		print(line)
		if line[0]!='2':
			all.append(line)
		
print(all)

f = open ('allhistory.txt','a+')

for line in all :
        f.write(line)
f.close()
