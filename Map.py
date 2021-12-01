from LevelData import *
from genericpath import exists

def loadMapFrFile(fileName):
    if (exists(fileName)):
        loadMap = []
        file = open(fileName)
        fileLines = []
        fileLines = file.readlines()
        currentParser = 0
        mWidth = int(fileLines[0][0:2])
        mHeight = int(fileLines[0][3:5])

        for y in range(1,mHeight):
            temp = []
            currentParser = 0
            for x in range(0,mWidth):
                oldParser = currentParser
                currentParser = fileLines[y].find(" ", oldParser + 1, len(fileLines[y]))
                temp.append(int(fileLines[y][oldParser:currentParser]))
            loadMap.append(temp)
        file.close()
        return loadMap, True, mWidth, mHeight
    else:
        print("File not found.")
        return [], False, 0, 0

level = Map0