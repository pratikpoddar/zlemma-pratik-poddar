SMALL_NUM = 0.00

def floydwarshall(matrix, skills):

        skillset = []
        for skillx in skills:
                for skilly in skills:
                        try:
                                if matrix[skillx][skilly] > 0.02:
                                        skillset.append(skillx)
                                        skillset.append(skilly)
                        except:
                                pass
        skills = list(set(skillset))
	
	outputmatrix=matrix
	for skillx in skills:
		for skilly in skills:
			try:
				outputmatrix[skillx][skilly]=matrix[skillx][skilly]
			except:
				outputmatrix[skillx][skilly] = SMALL_NUM

	for skill in skills:
		outputmatrix[skill][skill] = 1.0

	for skill1 in skills:
		for skill2 in skills:
			for skill3 in skills:
				if outputmatrix[skill1][skill2]*outputmatrix[skill2][skill3] > outputmatrix[skill1][skill3]:
					outputmatrix[skill1][skill3] = outputmatrix[skill1][skill2]*outputmatrix[skill2][skill3]

	return outputmatrix


