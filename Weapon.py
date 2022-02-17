import math, NPC

def getDoor(doors, coords):
	for i in range(0, len(doors)):
		if math.sqrt(pow(doors[i].x + 0.5 - coords[0], 2) + pow(doors[i].y + 0.5 - coords[1], 2)) <= 0.5:
			return i
	return 0

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
        x, y = px, py
        stepSize = 0.01
        while True:
            x += stepSize * math.cos(angle)
            y += stepSize * math.sin(angle)
            doorID = getDoor(doors, [x, y])
            if (level[int(y)][int(x)] <= 899 and level[int(y)][int(x)] > 0) or (level[int(y)][int(x)] > 899 and level[int(y)][int(x)] <= 999 and not doors[doorID].isOpen):
                return math.sqrt(pow(px - x, 2) + pow(py - y, 2))

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
        else:
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
                if targVect[len(targVect)-1][1] <= self.rng:
                    if npcList[targVect[len(targVect)-1][0]].takeDamage(self.dmg):
                        npcList.append(NPC.NPC(npcList[targVect[0][0]].coords, 4002, len(npcList), 100))