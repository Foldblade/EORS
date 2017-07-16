#encoding:gb2312
import os

originfile = open(os.path.dirname(os.getcwd()) + "/cache/sentence.txt","r+")
fin = []
origin = originfile.readlines()
originfile.close()
#print(origin)
for obj in origin :
    #print(obj)
    if obj not in fin :
        fin.append(obj)
        #print(fin)

finfile = open(os.path.dirname(os.getcwd()) + "/cache/sentence.txt","w+")
finfile.close()
finfile = open(os.path.dirname(os.getcwd()) + "/cache/sentence.txt","a+")
for obj in fin :
    finfile.write(obj)
#originfile.write(fin)
finfile.close()
#print('done!')

allhistoryfile = open(os.path.dirname(os.getcwd()) + "/data/allhistory.txt","r+")
allhistory = allhistoryfile.readlines()
allhistoryfile.close()
#print(allhistory)
cachefile = open(os.path.dirname(os.getcwd()) + "/cache/sentence.txt","r+")
cache = cachefile.readlines()
cachefile.close()
#print(cache)
newcache=[]

for obj in cache :
    #print(obj)
    if obj not in allhistory :
        newcache.append(obj)
        #print(newcache)

finfile = open(os.path.dirname(os.getcwd()) + "/cache/sentence.txt","w+")
finfile.close()
finfile = open(os.path.dirname(os.getcwd()) + "/cache/sentence.txt","a+")
for obj in newcache :
    finfile.write(obj)

finfile.close()
#print('done!')
