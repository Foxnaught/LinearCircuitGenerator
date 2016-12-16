from copy import deepcopy

#Returns a list of how many elements total are in the component and how many nested lists there are
def listSum(list, depth=1):
	#Sum = complexity[0], nests = complexity[1]
	#Sum is the total number of resistors in configuration
	#Nests is the number of nested lists
	complexity = [0,0]
	for item in list:
		if type(item) == int:
			complexity[0] += item * depth
		else:
			complexity[1] += 1
			if type(item) == int:
				next = [0,1]
			else:
				next = listSum(item, depth+1)
			#Sum
			complexity[0] += next[0]
			#number of nested lists
			complexity[1] += next[1]
	
	return complexity



#This function is designed to align the lists in such a way that a simple comparison can determine them to be duplicates
#It does not catch them all as the rules have ambiguous cases. (checkItems() finds the rest of the duplicates, but the recursion is costly)


#Organize a list of nested lists from least to greatest in complexity of elements (Number of lists contained)
#and total elements (straight count of all resistors in the element of the list)
def listSort(root):
	tempList = [root[0]]
	#These are all local variable place-holders for outside functions for speed. (insertItem(someVariable) is the same as tempList.inser(someVariable))
	insertItem = tempList.insert
	reverseList = tempList.reverse
	appendItem = tempList.append
	newList = root[1:]
	for index1, item1 in enumerate(newList):
		lastItem = tempList[-1]
		#If the last item in tempList is an integer then there is no need to compare lengths,
		#the integer will be as simple or simpler than the appended value
		if type(lastItem) == int:
			appendItem(item1)
		#If the appended value is an integer then prepend it
		elif type(item1) == int:
			insertItem(0, item1)
		#we are looking at two lists then
		else:
			cIndex = -1
			
			#Loop through the new sorted list (Starts out blank and is passed over once)
			for i,rItem in enumerate(tempList):
				if type(rItem) != int:
					if type(rItem) == int:
						rList = [0,1]
					else:
						rList = listSum(rItem)
					
					if type(item1) == int:
						cList = [0,1]
					else:
						cList = listSum(item1)
					
					#We are starting from the least complex part of the newly sorted list
					#We will proceed until the item to be added is less complex than the next position
					#If the sum of the resistors in 
					n = len(rItem)
					n2 = len(item1)
					if n > n2:
						cIndex = i
						break
					elif n == n2:
						#If the sum of the addon is greater than the sum of the current index,
						#Then record this index so we can insert right before it.
						if rList[1] > cList[1]:
							cIndex = i
							break
						#If the sums are equal but the complexities (number of nested lists) are not, then order by complexity
						elif rList[1] == cList[1] and rList[0] > cList[0]:
							cIndex = i
							break
						
			
			#If the index is zero then inserting isn't appropriate, so we prepend
			if cIndex == -1:
				appendItem(item1)
			else:
				insertItem(cIndex, item1)

	
	#if(len(root) != len(tempList)):
	#	print("Broken sorter")
	
	return tempList

def arrange(nList, mainLine=[], header=0):
	combos = [nList]

	if len(nList) > 2:
		for i in range(0, len(nList)-1):
			for t in range(i+1, len(nList)):
				testList = deepcopy(nList)
				del testList[t]
				del testList[i]

				if [[nList[i], nList[t]]] + testList not in mainLine + combos:
					combos += arrange([[nList[i], nList[t]]] + testList, mainLine + combos)

				if nList[i] != 1:
					if nList[t] != 1:
						if [nList[i] + nList[t]] + testList not in mainLine + combos:
							combos += arrange([nList[i] + nList[t]] + testList, mainLine + combos)
					else:
						tempItem = deepcopy(nList[i])
						tempItem.append(nList[t])
						if [tempItem] + testList not in mainLine + combos:
							combos += arrange([tempItem] + testList, mainLine + combos)

				if nList[t] != 1:
					if nList[i] != 1:
						if [nList[t] + nList[i]] + testList not in mainLine + combos:
							combos += arrange([nList[t] + nList[i]] + testList, mainLine + combos)
					else:
						tempItem = deepcopy(nList[t])
						tempItem.append(nList[i])
						if [tempItem] + testList not in mainLine + combos:
							combos += arrange([tempItem] + testList, mainLine + combos)

	return combos

#This will determine if a complex list is identical on every level regardless of order of elements
#This only works on lists with the same number of total elements
def checkItems(listArg1, listArg2):
	#Make localized variables so we don't affect the lists outside the function
	list1 = listArg1
	list2 = listArg2[:]
	n = len(list1)
	n2 = len(list2)
	
	#We are going to loop though each item in the first list and compare it to each item in the second
	found = False
	foundIndex = 0
	counter = 0
	#If the shallowest level of the lists doesn't match in length then there is no way they are equivalent
	if n == n2:
		#Loop through list1 and try to match its elements to elements in lists 2
		#If the number of matched elemetns is equal to the length of list1, then they are equal.
		
		#The behavior of the function is difficult to describe when it encounters elements of a list that are also lists.
		#It recursively calls itself on the element and an element from the other list.
		#If those subsequent lists are simple (no list elements), they are compared normally and the result is added (or not) to the counter of the parent function call.
		#If they are not simple, the process starts again.
		for item1 in list1:
			found = False
			foundIndex = 0
			#To prevent counting the same items again, after an element in list2 is found to match,
			#the index of the matching element is removed from list2 for the next item1 in list1 to be compared
			for iter, item2 in enumerate(list2):
				
				#If both values are integers then compare them
				if type(item1) == int:
					#Make sure the second value is an integer otherwise they do not match
					if type(item2) == int:
						if item1 == item2:
							found = True
							#make sure we save where we are so we don't count this again
							foundIndex = iter
							#prematurely end the loop
							break
							
				#If both values are lists, compare them through recursion
				else:
					#We already know item1 is a list, if this one isn't then it won't match
					#if it is a list then we must compare the lists
					if type(item2) != int:
						#This is a direct comparison
						if item1 == item2:
							found = True
							foundIndex = iter
							break
						#This recurses to deeper levels of the lists to ensure they are not duplicates
						elif checkItems(item1, item2):
							
							found = True
							#make sure we save where we are se we don't count this again
							foundIndex = iter
							#prematurely end the loop
							break
				#Keep track of what iteration we are on
				
				
				
			#If we found a match for a value in list 1, incremenet our counter
			if found:
				counter += 1
				#We pop the value from the second list so it is not counted twice when we loop through it again
				list2.pop(foundIndex)
	
	#If the count of the resistors in both lists is equal then return true
	return (counter == n)


n = int(input("Number of resistors: "))
series = [1] * n

perms = arrange(series)
unique = []
for p in perms:
	if listSort(p) not in unique:
		found = False
		for u in unique:
			if checkItems(p, u):
				found = True
				#print(p)
				#print(u)
				#print(listSort(p))
		
		if not found:
			unique.append(listSort(p))

print(len(unique) * 2)