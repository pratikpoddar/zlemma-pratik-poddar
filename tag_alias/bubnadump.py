import json
import pickle

f = []
file=open('stackoverflowtagaliasfinalrenamed.json', 'r')
f+=[json.load(file)]
file.close()

file=open('mathtagaliasfinalrenamed.json', 'r')
f+=[json.load(file)]
file.close()

file=open('quanttagaliasfinalrenamed.json', 'r')
f+=[json.load(file)]
file.close()

g = dict(dict(f[2], **f[1]), **f[0])

file=open('bubnadump.json', 'w')
json.dump(g, file)
file.close()

file=open('Skill_data(ajitdump.list).dict','r')
permitted = json.load(file)
file.close()

permitted.items()
permitted = map(lambda y: y[0], filter(lambda x: x[0] == x[1]['alternate_name'], permitted.items()))

h = dict(filter(lambda x: x[0] in permitted, g.items()))
file=open('bubnadumpcurated.json', 'w')
json.dump(h, file)
file.close()

file=open('renamedcomplete.txt','r')
i = json.load(file)
file.close()
j = list(set(i.keys())-set(h.values()))
file=open('tagswithnoalias.pickle', 'w')
pickle.dump(j, file)
file.close()



