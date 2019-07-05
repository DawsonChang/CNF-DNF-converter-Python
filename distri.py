import re
from formulaTransform import getOrderList, getOriginalFormula, removeBrackets
from simpli import deleteSameVar, deleteContradictionVar, deleteSameSentence

def runDistributionEachElement(orderList, index):
	remainString = orderList[index]
	firstVar = ""
	secondVar = ""
	mainSymbol = ""
	str1 = ""
	temp1 = []
	temp2 = []
	resultList = []

	while remainString:
		# print("remainString: " + remainString)
		if len(remainString) == 1:
			secondVar = remainString
			remainString = ""		
			# print("remainString: " + remainString)
		else:
			reg = '(.*?)\s+(and|or)\s+(.*)'
			gotReg = re.search(reg, remainString)

			if gotReg:
				firstVar = gotReg.group(1)
				mainSymbol = gotReg.group(2)
				secondVar = gotReg.group(3)
				
				if ("and" in gotReg.group(3)) or ("or" in gotReg.group(3)):
					remainReg = re.search("(.*?)\s+(and|or)\s(.*)", gotReg.group(3))
					secondVar = remainReg.group(1)
					remainString = gotReg.group(3)
				else:
					remainString = ""

		# print("firstVar: " + firstVar)
		# print("secondVar: " + secondVar)

		
		if len(temp1) == 0:
			if firstVar.isnumeric():
				temp1 = orderList[int(firstVar)].split()
			else:
				temp1.append(firstVar)

		temp2 = []
		if secondVar.isnumeric():
			temp2 = orderList[int(secondVar)].split()
		else:
			temp2.append(secondVar)

		inBracketSymbol = "or" if ("or" in temp1 or "or" in temp2) else "and"
		# print("inBracketSymbol: " + inBracketSymbol)
		resultList = []
		newString = ""
		nextNeg = False
		flag = False
		for elem1 in temp1:
			newString = ""
			if elem1 != "or" and elem1 != "and":
				if elem1 == "~":
					nextNeg  = True
				else:
					if nextNeg:
						newString = "~ " + elem1 + " " + mainSymbol + " "
					else:
						newString = newString + elem1 + " " + mainSymbol + " "

					for elem2 in temp2:
						if elem2 != "or" and elem2 != "and":
							if elem2 == "~":
								flag = True
							else:
								if flag:
									newString2 = newString + "~ " + elem2
									flag = False
								else:
									newString2 = newString + elem2
								# print("newString2: " + newString2)
								resultList.append(newString2.rstrip())
								resultList.append(inBracketSymbol)
					nextNeg = False

		resultList.pop()
		# print(resultList)
		temp1 = resultList
	#-----------end of while loop----------
	finalString = resultList[0]
	
	if orderList[index] != resultList[0]:
		for i, elem in enumerate(resultList):
			if i % 2 == 0:
				resultList[i] = "(" + elem + ")"

		finalString = ' '.join(resultList)
	# print(finalString)
	# print("finalString: " + finalString)
	orderList[index] = finalString
	formula = getOriginalFormula(orderList)
	# print("formula: " + formula)
	orderList = getOrderList(formula)
	# print(orderList)
	#indexMax = len(orderList)
	formula = removeBrackets(orderList)
	orderList = getOrderList(formula)

	return orderList


def distribution(orderList):
	indexMax = len(orderList)
	# print(indexMax)
	index = 0
	formula = orderList[-1]
	while index < indexMax - 1:

		if re.search("\d+", orderList[index]):
			orderList = runDistributionEachElement(orderList, index)

		index += 1
		# print("index: " + str(index))
		# print("len(orderList): " + str(len(orderList)))
		indexMax = len(orderList)
	#----------end of while loop----------
	return removeBrackets(orderList)

def changeToOppositeForm(orderList):

	#(a or b) and (c or d)
	# = ((a and c) or (a and d) or (b and c) or (b and d))
	orderList = runDistributionEachElement(orderList, -1)

	# print(orderList)
	# getOriginalFormula(orderList)
	orderList = deleteSameVar(orderList)
	# print(getOriginalFormula(orderList))
	orderList = deleteContradictionVar(orderList)
	# print(getOriginalFormula(orderList))
	orderList = deleteSameSentence(orderList)
	# print(getOriginalFormula(orderList))


	#remove the list which has only one number from the back
	while re.search('^\d+$', orderList[-1]):
		orderList.pop()
	# print(orderList)
	return orderList
