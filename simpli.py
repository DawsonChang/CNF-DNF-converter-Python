import re

def deleteSameVar(orderList):
	for index, elem in enumerate(orderList):
		if index == len(orderList)-1:
			break
		tempList = elem.split()
		for i, item in enumerate(tempList):
			if item == "~":
				tempList[i+1] = "~ " + tempList[i+1]
				del tempList[i]

		symbol = ""
		for item in tempList:
			if item == "or":
				symbol = " or "
				tempList.remove("or")
				continue
			elif item == "and":
				symbol = " and "
				tempList.remove("and")
				continue
			tempList = [x for x in tempList if x != item]
			tempList.append(item)

		tempList.sort()
		newString = ""
		for item in tempList:
			newString = newString + item + symbol
		
		endPoint = 0 - len(symbol)
		newString = newString[:endPoint]
		# print("newString:", end="")
		# print(newString)
		orderList[index] = newString

	return orderList

def deleteContradictionVar(orderList):
	length = len(orderList)
	index = 0
	while index < length:
		if orderList[-1] == "0":
			orderList.pop()
			length -= 1
		if len(orderList) == 1:
			index = 0

		# print("index:{} length:{}".format(index, length))
		# print(orderList)
		elem = orderList[index]
		tempList = elem.split()
		for i, item in enumerate(tempList):
			if item == "~":
				tempList[i+1] = "~ " + tempList[i+1]
				del tempList[i]

		symbol = ""
		for item in tempList:
			if item == "or":
				symbol = " or "
				tempList.remove("or")
				continue
			elif item == "and":
				symbol = " and "
				tempList.remove("and")
				continue

		if symbol == " or ":
			for item in tempList:
				if "~" not in item: 
					negItem = "~ " + item
					if negItem in tempList:
						del orderList[index]
						if len(orderList) == 0:
							orderList.append("True")
							break
						index -= 1
						lastNumber = str(length - 2)
						length -= 1
						m = re.search('^(.*?)' + " and " + lastNumber + '(.*)$', orderList[-1])
						if m:
							orderList[-1] = m.group(1) + m.group(2)
						break
				else:
					continue

		elif symbol == " and ":
			for item in tempList:
				if "~" not in item: 
					negItem = "~ " + item
					if negItem in tempList:
						del orderList[index]
						if len(orderList) == 0:
							orderList.append("False")
							break
						index -= 1
						lastNumber = str(length - 2)
						length -= 1
						m = re.search('^(.*?)' + " or " + lastNumber + '(.*)$', orderList[-1])
						if m:
							orderList[-1] = m.group(1) + m.group(2)
						break
				else:
					continue

		index += 1

	# print("orderlist: ", end="")
	# print(orderList)
	return orderList

def deleteSameSentence(orderList):
	length = len(orderList)
	i = 0
	symbol = ""
	if "or" in orderList[-1]:
		symbol = "or"
	elif "and" in orderList[-1]:
		symbol = "and"
	while i < length - 1:
		j = i + 1
		while j < length - 1:
			if(orderList[i] == orderList[j]):
				del orderList[j]
				lastNumber = str(length - 2)
				length -= 1
				m = re.search('^(.*?)\s' + symbol + " " + lastNumber + '(.*)$', orderList[-1])
				orderList[-1] = m.group(1) + m.group(2)
			else:
				j += 1
		i += 1

	return orderList
