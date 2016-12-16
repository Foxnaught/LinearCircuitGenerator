import time, math

#Program starts at main()

#A circuit configuration is a series of nested lists. The lists alternate between a list of elements in series and lists of elements in parallel.
#If you have traversed an odd number of lists including the outer-most shell then you are in a series list. If even, then it is in parallel


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


#This recursively combines and returns combinations of a given resistor configuration
#The default is a straight series

#The variable mainLine holds the current list of configurations of all the parent functions.
#This reduces the amount of duplicate results by allowing the function to be more aware of its position in the process
def arrangeComponents(resistors, mainLine):
	components = []
	n = len(resistors)
	firstList = []
	secondList = []
	#Python runs local variables much faster
	#Type appendFirst(someVariable) is the same as firstList.append(someVariable) now and is slightly faster
	appendFirst = firstList.append
	appendSecond = secondList.append
	
	#This function will recurse until there is only one parallel component in the configuration
	#This section configures each component in parallel with every other individual component
	for fIndex,first in enumerate(resistors):
		if first not in firstList:
			#Add this item to the firstList so we don't use it again
			appendFirst(first)
			del secondList[:]
			
			for sIndex,second in enumerate(resistors):
				#Make sure to not pair the same component to itself
				#and not to pair two components that we have already paired
				if(fIndex != sIndex):
					if second not in secondList:
						#Add this item to the secondList so we don't use it again
						appendSecond(second)
						
						#Place a copy of the initial configuration into tempRes
						tempRes = resistors[:]
						#Pop the two components being placed in parallel and series
						firstComp = tempRes.pop(fIndex)
						if sIndex > fIndex:
							sIndex -= 1
						secondComp = tempRes.pop(sIndex)
						
						#Copy the leftover series for appending the parallel component later
						t = tempRes[:]
						
						#This section places them in order as separate elements on the same level
						if type(firstComp) == int:
							tempRes.append([firstComp, secondComp])
						elif type(secondComp) == int:
							tempRes.append([secondComp, firstComp])
						else:
							tempRes.append(listSort([firstComp, secondComp]))
						#Sort the list from least to most complex, this makes comparison and duplicate finding much easier.
						if n > 2:
							tempRes = listSort(tempRes)
						#Store the current configuration
						store = True
						
						#If we have already encountered this configuration before in our mainline (the variable containing resistor lists from parent calls)
						#Then don't bother adding sorting or adding it to our list of configurations
						for i in mainLine:
							if i == tempRes:
								store = False
								break
						
						if store:
							#If we didn't already find a sorted configuration that matches this one, append it to the list of total configurations
							components.append(tempRes)
						
						#Recurse with new configuration and store results
						if n > 2 and store:
							#Components, which stores the list of current resistors, is now passed to the next level so that duplicates are not added to the list
							newC = arrangeComponents(tempRes, components)
							#This adds the configurations obtained by the child arrangeComponents call to the main list of configurations
							components.extend(newC)
						

						#This section combines the child elements of each list item into one item and appends it to the resistors not being altered
						#If the first resistor is not a list then it has already been attempted above
						if type(firstComp) != int:
							para = firstComp[:]
							
							para.append(secondComp)
							para = listSort(para)
							
							
							t.append(para)
							if n > 2:
								t = listSort(t)
							#store the current configuration
							store = True
							for i in mainLine:
								if i == t:
									store = False
									break
									
							if store:
								components.append(t)
									
							#Recurse the new configuration
							if n > 2 and store:
								components.extend(arrangeComponents(t, components))
								
	#This returns the total list of configurations for this and all recursive child calls
	return components

def getResistance(config, series=True):
	res = 0
	for i in config:
		if series:
			if isinstance(i, int):
				res += i
			else:
				res += getResistance(i, not series)

		else:
			if isinstance(i, int):
				res += 1/i
			else:
				res += 1/getResistance(i, not series)

	if not series:
		res = 1/res

	return res



#Returns a list of how many elements total are in the component and how many nested lists there are
def listSum(list, depth=1):
	#Sum = complexity[0], nests = complexity[1]
	#Sum is the total number of resistors in configuration
	#Nests is the number of nested lists
	complexity = [0,0]
	for item in list:
		if type(item) == int:
			#We square the depth to help create bias
			complexity[0] += item * depth * depth
		else:
			#this would normally iterate one but we iterate by depth to create a bias towards one list over another
			complexity[1] += depth*depth
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
#We want to do this in a biased and deterministic way such that complex nested lists with equivalent items at equivalent depths will be arranged into one form
#This simplifies comparison of lists when looking for duplicates
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
		#The integer will be as simple or simpler than the value we are going to append
		#Because we are trying to create a list going from least to most complex
		if type(lastItem) == int:
			appendItem(item1)
		#If the appended value is an integer then prepend it
		elif type(item1) == int:
			insertItem(0, item1)
		#we are looking at two lists then
		#This is a complex issue
		else:
			cIndex = -1
			
			#Loop through the new sorted list (Starts out blank and is passed over once)
			for i,rItem in enumerate(tempList):
				if type(rItem) != int:
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


#Builds a simple series of values in a list [1,1,1,1,1,...]
#This could likely be optimized further if each list were compressed into a simple integer I.E. [1,1,[1,1],[1,1,1]] => [2,[2],[3]]
def makeSeries(nSeries, commonResistance=1):
	series = []
	for i in range(nSeries):
		series.append(commonResistance)
	
	return series

#Only return a list of elements that aren't already in root
def getUnique(root):
	#The list that will store our unique elements
	unique = []
	#The list that will store examples of disimilar but equivalent lists (parallel and series elements are out of order)
	bad = []
	calList = []
	appendItem = unique.append
	#for each item in the list
	for item in root:
		#If the item is not in our uniqueList, it is not a duplicate
		if item not in unique:
			appendItem(item)

	return unique

def getConfigurations(n):
	#make a component with a basic series with the number of resistors
	#Run the basic series configuration through a recursive function that will return a list of all possible permutations
	#duplicates included
	configurations = arrangeComponents(makeSeries(n), [])
	#Return list of non-duplicates
	return getUnique(configurations)



#This is where it starts
def main():
	#Main()
	checkInput = True
	#Keep attempting input until an integer is received
	while(checkInput):
		print("Enter the number of resistors: ")
		try:
			nInit = int(input())
			checkInput = False
		except:
			print("Integers only!")

	checkInput = True
	while(checkInput):
		print("Enter the resistance to approximate: ")
		try:
			resistanceGoal = float(input())
			checkInput = False
		except:
			print("Decimals only!")


	
	#This is where we start the program's clock time
	startTime = time.time()
	
	#All unique configurations are stored in the configs variable
	configs = getConfigurations(nInit)
	for a in range(len(configs)):
		for b in configs[a+1:]:
			if checkItems(configs[a], b):
				print(configs[a])
				print(b)
				print("Match")

	configs.append(makeSeries(nInit))

	closestResistance = 0
	closestConfig = []
	for c in configs:
		if math.fabs(closestResistance - resistanceGoal) > math.fabs(getResistance(c) - resistanceGoal):
			closestResistance = getResistance(c)
			closestConfig = c
	
	print("Approximate Resistance: " + str(closestResistance))
	print(closestConfig)
	
	#This chunk overwrites or creates a file called "configList.txt" in the same directory as the python file
	file = open("configList.txt", "w")
	for i in configs:
		file.write("[" + ','.join(str(v) for v in i) + "]")
		file.write("\n")
	file.close()
	
	#Print how many
	#no duplicates
	print("Number of configurations: ")
	print(len(configs))
	#Show the execution time
	endTime = (time.time() - startTime)
	print(str(endTime) + " seconds")


#Go up ^ to "def main():"
main()
