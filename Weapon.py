import math, NPC, Sound, configparser, sys
from Sound import *

def getDoor(doors, coords):
	for i in range(0, len(doors)):
		if math.sqrt(pow(doors[i].x + 0.5 - coords[0], 2) + pow(doors[i].y + 0.5 - coords[1], 2)) <= 0.8:
			return i
	return 0

def createWeaponList(weapSpriteList, boomList):
    weaponList = {}
    cfg = configparser.ConfigParser()
    cfg.read('gfx.conf')
    for option in cfg['WEAPONS']:
        print(option)
        values = cfg['WEAPONS'][option].split(',')
        for i in range(0, len(values)):
            values[i] = int(values[i])
        weaponList[int(option)] = Weapon(values[0], values[1], values[2], values[3], values[4], weapSpriteList[values[0]], boomList)
        #Weapon(1, 25, 8, 4, 0, weaponSpriteList[1], boomList),
    return weaponList

class Weapon:
    def __init__(self, id, dmg, rng, sprd, ammoID, sprite, boomList):
        self.id = id
        self.dmg = dmg
        self.rng = rng
        self.sprd = sprd
        self.sprite = sprite
        self.ammoID = ammoID

        self.shotFrame = -1

        self.yOffset = 0

        #Dictionary used to calculate the yOffset for good recoil
        self.velocityIndex = {
            0 : -3,
            1 : -2,
            2 : -1,
            3 :  0,
            4 : 0.1,
            5 : 0.6,
            6 : 1,
            7 : 1.3,
            8 : 1.2,
            9 : 1.1,
        }
        
        #Dictionary used to animate the sprite correctly
        self.animationIndex = [1,2,3,3,2]

        #Set the current sprite to default
        self.currentSprite = sprite[0]

        self.boomList = boomList

    #Bubble sort, used to sort the list of sprites to draw
    def Sort(self, vect):
        for i in range(0,len(vect)):
            for k in range(0,len(vect) - 1):
                if (vect[k][1] > vect[k+1][1]):
                    vect[k], vect[k+1] = vect[k+1], vect[k]
        return vect


    #Raycast check wall(simple, not a lot of checks)
    def checkWallDist(self, px, py, angle, level, doors):

        #Casting 1 ray to test functionality
        rayAng = angle

        #These booleans will run our while loops 
        horizCollision = False
        vertCollision = False

        #Keeps track of the distance from player to wall
        horizDist = 0.0
        vertDist = 0.0
        drawDist = 0.0

        #Resetting variables
        x = px
        y = py

        cX = 0
        cY = 0

        dX = 0
        dY = 0

        #Horizontal line checks
        #Is the player looking up or down? We have different distance to the next y integer point depending on the characters facing. Let's calculate those values.
        #Camera is looking up
        if rayAng >= math.pi:
            cY = int(py) - py
            dY = -1
            
        #Camera is looking down
        elif rayAng < math.pi:
            cY = int(py + 1) - py
            dY = 1

        #Calculate the change in x to the next integer from the starting position, as well as the change in x afterwards
        #If statement to verify that there will not be a divide by zero error
        if math.tan(rayAng != 0):
            cX = cY / math.tan(rayAng)
            dX = dY / math.tan(rayAng)

        #Adjust (x,y) to the edge of the current tile the player is in, in the direction he is facing
        x += cX
        y += cY

        #Increment through steps, testing each horizontal line where y is an integer
        while (horizCollision == False):

            #Prevent out of bound error while looking through map array
            if int(y) >= len(level) or int(x) >= len(level[0]) or int(y) < 0 or int(x) < 0:
                horizDist = math.sqrt(pow(x-px,2) + pow(y-py,2))
                horizCollision = True

            #Is the player looking up or down? This matters because the tile is seen as the top edge,
            #if we do not subtract 1 from y when looking up, it will look 1 block past where it should.
            #Player looking up
            elif rayAng >= math.pi:

                #Collision? If yes, break loop and have distance value set
                if (level[int(y-1)][int(x)] > 0 and level[int(y-1)][int(x)] <= 899):
                    horizDist = math.sqrt(pow(x-px,2) + pow(y-py,2))
                    horizCollision = True

                #DOOR CHECK
                elif (level[int(y-1)][int(x)] > 899 and level[int(y-1)][int(x)] <= 999):
                    
                    currentTile = level[int(y-1)][int(x)]

                    doorID = getDoor(doors, [int(x), int(y-1)])
        
                    if int(y + 0.5*dY) < len(level) and int(y + 0.5*dY) >= 0 and int(x + 0.5*dX) < len(level) and int(x + 0.5*dX) >= 0:# and not doors[doorID].isOpen:				
                        if (level[int(y - 1 - 0.5*dY)][int(x + 0.5*dX + doors[doorID].offset)] == currentTile):
                            horizDist = math.sqrt(pow(x-px,2) + pow(y-py,2)) + 0.5
                            horizCollision = True
                        else:
                            x += dX
                            y += dY
                    else:
                        x += dX
                        y += dY

                #Otherwise, keep incrementing
                else:	
                    x += dX
                    y += dY

            #Camera looking down
            elif rayAng < math.pi:

                #Collision? If yes, break loop and have distance value set
                if (level[int(y)][int(x)] > 0 and level[int(y)][int(x)] <= 899):
                    horizDist = math.sqrt(pow(x-px,2) + pow(y-py,2))
                    horizCollision = True
                
                #DOOR CHECK
                elif (level[int(y)][int(x)] > 899 and level[int(y)][int(x)] <= 999):
                    
                    currentTile = level[int(y)][int(x)]

                    doorID = getDoor(doors, [int(x), int(y)])
                    
                    if int(y + 0.5*dY) < len(level) and int(y + 0.5*dY) >= 0 and int(x + 0.5*dX) < len(level) and int(x + 0.5*dX) >= 0:# and not doors[doorID].isOpen:
                        if (level[int(y + 0.5*dY)][int(x + 0.5*dX + doors[doorID].offset)] == currentTile):
                            horizDist = math.sqrt(pow(x-px,2) + pow(y-py,2)) + 0.5
                            horizCollision = True
                        else:
                            x += dX
                            y += dY
                    else:
                        x += dX
                        y += dY
                
                #Otherwise, keep incrementing
                else:	
                    x += dX
                    y += dY

        #Resetting variable values
        x = px
        y = py

        cX = 0
        cY = 0

        dX = 0
        dY = 0

        #Vertical line checks
        #Is the player looking right or left? We have different distance to the next x integer point depending on the characters facing. Let's calculate those values.
        #Camera is looking left
        if rayAng >= math.pi / 2 and rayAng <= math.pi * 3/2:
            cX = int(px) - px
            dX = -1

        #Camera is looking right
        elif rayAng > math.pi * 3/2 or rayAng < math.pi / 2: #Looking right
            cX = int(px + 1) - px
            dX = 1

        #Calculate the change in y to the next integer from the starting position, as well as the change in y afterwards
        cY = cX * math.tan(rayAng)
        dY = dX * math.tan(rayAng)

        #Adjust (x,y) to the edge of the current tile the player is in, in the direction he is facing
        x += cX 
        y += cY

        #Increment through steps, testing each vertical line where x is an integer
        while (vertCollision == False):

            #Prevent out of bound error while looking through map array
            if int(y) >= len(level) or int(x) >= len(level[0]) or int(y) < 0 or int(x) < 0:
                vertDist = math.sqrt(pow(x-px,2) + pow(y-py,2))
                vertCollision = True

            #Is the player looking left or right? This matters because the tile is seen as the left edge,
            #if we do not subtract 1 from x when looking left, it will look 1 block past where it should.
            #Player looking left
            elif rayAng >= math.pi / 2 and rayAng <= math.pi * 3/2:
                #Collision? If yes, break loop and have distance value set
                if (level[int(y)][int(x-1)] > 0 and level[int(y)][int(x-1)] <= 899):
                    vertDist = math.sqrt(pow(x-px,2) + pow(y-py,2))
                    vertCollision = True

                #DOOR CHECK
                elif (level[int(y)][int(x-1)] > 899 and level[int(y)][int(x-1)] <= 999):
                    
                    currentTile = level[int(y)][int(x-1)]

                    doorID = getDoor(doors, [int(x), int(y)])
                    
                    if int(y + 0.5*dY) < len(level) and int(y + 0.5*dY) >= 0 and int(x + 0.5*dX) < len(level) and int(x + 0.5*dX) >= 0:# and not doors[doorID].isOpen:
                        if (level[int(y + 0.5*dY + doors[doorID].offset)][int(x - 1 - 0.5*dX)] == currentTile):
                            vertDist = math.sqrt(pow(x-px,2) + pow(y-py,2)) + 0.5
                            vertCollision = True
                        else:
                            x += dX
                            y += dY
                    else:
                        x += dX
                        y += dY

                #Otherwise, continue incrementing
                else:	
                    x += dX
                    y += dY

            #Player looking right
            elif rayAng > math.pi * 3/2 or rayAng < math.pi / 2:	

                #Collision? If yes, break loop and have distance value set
                if (level[int(y)][int(x)] > 0 and level[int(y)][int(x)] <= 899):
                    vertDist = math.sqrt(pow(x-px,2) + pow(y-py,2))
                    vertCollision = True
                            
                #DOOR CHECK
                elif (level[int(y)][int(x)] > 899 and level[int(y)][int(x)] <= 999):
                    
                    currentTile = level[int(y)][int(x)]

                    doorID = getDoor(doors, [int(x), int(y)])
                    
                    if int(y + 0.5*dY) < len(level) and int(y + 0.5*dY) >= 0 and int(x + 0.5*dX) < len(level) and int(x + 0.5*dX) >= 0:# and not doors[doorID].isOpen:
                        if (level[int(y + 0.5*dY + doors[doorID].offset)][int(x + 0.5*dX)] == currentTile):
                            vertDist = math.sqrt(pow(x-px,2) + pow(y-py,2)) + 0.5
                            vertCollision = True
                        else:
                            x += dX
                            y += dY
                    else:
                        x += dX
                        y += dY

                #Otherwise, keep incrementing
                else:	
                    x += dX
                    y += dY

        #Most of the time, vertical distance and horizontal distance will be different.
        #We want to render using the shorter value, because it is the first intersection.
        if (vertDist >= horizDist):
            drawDist = horizDist
        elif (vertDist < horizDist):
            drawDist = vertDist

        #Return the distance from the 
        return drawDist
        
    def Animate(self, frameCount):
        #Don't animate if it isn't necessary, shotFrame is the frame where the player pressed the shoot button, it is -1 by default
        if self.shotFrame == -1: 
            return
        #If the animation is currently underway in its 10 frame lifetime
        elif frameCount - self.shotFrame <= 9:
            #Change the current sprite to the one necessary for animation, it should change every 2 frames
            self.currentSprite = self.sprite[self.animationIndex[int((frameCount - self.shotFrame) / 2)]]

            #Update the yOffset
            self.yOffset += 10*self.velocityIndex[frameCount - self.shotFrame]
        else:
            self.shotFrame = -1
            self.yOffset = 0
            self.currentSprite = self.sprite[0]
    
    def resetYOffset(self):
        self.yOffset = 0
        self.currrentSprite = self.sprite[0]

    def Shoot(self, player, npcList, level, shotFrame, doors):
        #Verify that the player has ammo
        if player.ammoCount[self.ammoID] <= 0:
            return
        elif player.isAlive:

            Sound.Shoot_Sound(self.id)

            player.ammoCount[self.ammoID] -= 1

            x, y, angle = player.x, player.y, player.angle
            #Reset yOffset
            self.resetYOffset()

            #Notate the frame the shot was fired on
            self.shotFrame = shotFrame

            #Create empty list of objects to draw
            targVect = []
            
            #Cycle through every object
            for i in range(0,len(npcList)):
                if npcList[i].type >= 2000 and npcList[i].type < 3000:
                    #Determine object angle from origin line at camera position
                    objAngleFromOrig = math.atan((npcList[i].y - y) / (npcList[i].x - x))
                    if npcList[i].x - x < 0:
                        objAngleFromOrig += math.pi

                    #Calculate difference between object angle and camera facing
                    angleDiff = objAngleFromOrig - angle

                    #Adjust values accordingly to fall within trig parameters
                    while objAngleFromOrig > math.pi * 2:
                        objAngleFromOrig -= math.pi * 2
                    while objAngleFromOrig < 0:
                        objAngleFromOrig += math.pi * 2

                    while angleDiff < 0:
                        angleDiff += math.pi * 2
                    while angleDiff > math.pi:
                        angleDiff -= math.pi * 2

                    #If the difference in angle falls within the FOV
                    if abs(angleDiff) <= self.sprd * math.pi/180:
                        
                        #Calculate obj dist and the distance to the nearest wall
                        distToObj = math.sqrt(pow(npcList[i].x - x, 2) + pow(npcList[i].y - y, 2))
                        distToWall = self.checkWallDist(x, y, objAngleFromOrig, level, doors)

                        #If the object is closer than the nearest wall, add to draw vector
                        if distToWall > distToObj:
                            targVect.append([i, distToObj])

            #Sort things by how close they are
            self.Sort(targVect)

            #Apply damage to closest NPC
            if not targVect == []:
                if targVect[0][1] <= self.rng:
                    if npcList[targVect[0][0]].takeDamage(self.dmg):
                        npcList.append(NPC.NPC(npcList[targVect[0][0]].coords, 4002, len(npcList), 100))