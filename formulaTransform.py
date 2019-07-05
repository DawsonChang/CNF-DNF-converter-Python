import re
from simpli import deleteSameVar, deleteContradictionVar, deleteSameSentence

def intoBrackets(source, index):
	reg = '\(([^\(]*?)\)'
	gotReg = re.search(reg, source)
	if gotReg is None:
		return None, None
	new_source = re.sub(reg, str(index), source, count=1)
	# print(gotReg.group(1))
	return new_source, gotReg.group(1)

def getOrderList(formula):
	orderList = []
	final = formula
	while 1:
		formula, temp = intoBrackets(formula, len(orderList))
		if formula is None:
			break
		final = formula
		orderList.append(temp)

	orderList.append(final)
	return orderList

def getOriginalFormula(orderList):
	#tempFormula has the form of formula but with number
	#this method is to get the original formula from orderList
	tempFormula = orderList[-1]
	while 1:
		for num in re.findall("\d+", tempFormula):
			#if the form of orderList[int(num)] is 'p' or '~ p', don't add brackets
			if re.search("^[a-zA-Z]$", orderList[int(num)]) or re.search("^~ [a-zA-Z]$", orderList[int(num)]):
				tempFormula = tempFormula.replace(num, orderList[int(num)], 1)
			else:
				tempFormula = tempFormula.replace(num, "(" + orderList[int(num)] + ")", 1)
		if not re.search("\d+", tempFormula):
			break
		
	return tempFormula

def removeBrackets(orderList):
	#if two adjacent brackets have same "and" "or", remove the brackets
	#e.g. ((~ p and q) or (~ p or r)) = ((~ p and q) or ~ p or r)
	def rec(string, orderListIndex):
		for num in re.findall("\d+", string):
			numIndex = string.find(num)
			symbol = "and" if ("and" in orderList[orderListIndex]) else "or"
			newString, symbolOfNext = rec(orderList[int(num)], int(num))
			
			if (symbol == "and") and (symbolOfNext == "and"):
				#string = string[0:numIndex] + newString + string[numIndex+1:]
				string = string.replace(num, newString, 1)
			elif (symbol == "or") and (symbolOfNext == "or"):
				#string = string[0:numIndex] + newString + string[numIndex+1:]
				string = string.replace(num, newString, 1)
			else:
				#string = string[0:numIndex] + "(" + newString + ")" + string[numIndex+1:]
				string = string.replace(num, "(" + newString + ")", 1)
			
		if "and" in orderList[orderListIndex]:
			symbolOfNext = "and"
			return string, symbolOfNext
		elif "or" in orderList[orderListIndex]:
			symbolOfNext = "or"
			return string, symbolOfNext
		else:
			return string, None

	tempFormula, symbol = rec(orderList[-1], -1)
	return tempFormula
def iff_imp_Convert(orderList):
	newList = orderList.copy()
	for i, string in enumerate(orderList):

		#for converting equivalent
		reg = '^(.*?)<->(.*?)$'
		iffReg = re.search(reg, orderList[i])
		if iffReg:
			a, b = iffReg.group(1).strip(), iffReg.group(2).strip()

			# P <-> Q = (~P v Q) ^ (P v ~Q)
			if ("~" in a) and ("~" in b):
				a = a.replace('~','').strip()
				b = b.replace('~','').strip()

				orderList[i] = "(" + a + " or ~ " + b + ") and (~ " + a + " or " + b + ")"
			elif ("~" in a) and ("~" not in b):
				a = a.replace('~','').strip()
				orderList[i] = "(" + a + " or " + b + ") and (~ " + a + " or ~ " + b + ")"
			elif ("~" not in a) and ("~" in b):
				b = b.replace('~','').strip()
				orderList[i] = "(~ " + a + " or ~ " + b + ") and (" + a + " or " + b + ")"
			else:
				orderList[i] = "(~ " + a + " or " + b + ") and (" + a + " or ~ " + b + ")"

		#for converting implication
		#p->q is not work  how to fix this?????
		reg = '^(.*?[^<])->\s*(.*?)$'
		impReg = re.search(reg, orderList[i])
		if impReg:
			a, b = impReg.group(1).rstrip(), impReg.group(2)
			if "~" in a:
				orderList[i] = a.replace('~','') + " or " + b
			else:
				orderList[i] = "~ " + a + " or " + b

	return orderList

def deMorgen_Convert(orderList):
	for i in range(len(orderList)):
		while 1:
			reg = "(.*?)~\s*(\d+)(.*)"
			deMorgenReg = re.search(reg, orderList[i])
			if deMorgenReg:
				#index refers to the index of the previous part which we want to use deMorgan's law on
				index = int(deMorgenReg.group(2))
				#update current part without negation(~)
				orderList[i] = deMorgenReg.group(1) + deMorgenReg.group(2) + deMorgenReg.group(3)
				tempList = orderList[index].split(" ")
				for j in range(len(tempList)):
					if j > 0 and tempList[j] == "or":
						tempList[j] = "and"
					elif j > 0 and tempList[j] == "and":
						tempList[j] = "or"
					elif j > 0:
						if re.search("^\w+$", tempList[j]) and tempList[j-1] != "~":
							tempList[j] = "~ " + tempList[j]
					elif j == 0:
						if re.search("^\w+$", tempList[j]):
							tempList[j] = "~ " + tempList[j]
				while "~" in tempList:
					tempList.remove("~")
				
				orderList[index] = ' '.join(tempList)

			else:
				break

	return orderList
