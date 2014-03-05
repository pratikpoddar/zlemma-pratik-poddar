import json

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


