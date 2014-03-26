import pickle

def setoutput(s1, s2, value, output):
	if s1 in output.keys():
			output[s1][s2] = value
	else:
		output[s1] = {}
		output[s1][s2] = value

	return output


def getGraph(filename):
	output = {}
	file=open(filename, 'r')
	course_list = pickle.load(file)
	for course in course_list:
		for i in range(0,len(course)-2):
			output = setoutput(course[i], course[i+1], 0.85, output)
			output = setoutput(course[i+1], course[i], 0.65, output)
	
	return output



