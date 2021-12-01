
#Will flip the map vertically, if needed for formatting.  Not currently used but could be useful so it was left in the code, just in case
def formatMap(focusMap):
	currentLevel = []
	formattedMap = []
	for y in range(len(focusMap)-1, -1, -1):
		for x in range(len(focusMap[0])-1, -1, -1):
			currentLevel.append(focusMap[y][x])
		else: 
			formattedMap.append(currentLevel)
			currentLevel = []
	return formattedMap

#Find player inside of focusMap by cycling through and replace this with an empty block
def findPlayer(focusMap):                                         
	for x in range(0,len(focusMap[0])):
		for y in range(0,len(focusMap)):
			if focusMap[y][x] == -1:
				focusMap[y][x] = 0
				return x + 0.5,y + 0.5
			else:
				continue
