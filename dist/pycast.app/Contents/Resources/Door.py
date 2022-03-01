import math

def findDoors(level):
    doors = [Door([-1, -1])]
    for x in range(0,len(level[0])):
        for y in range(0, len(level)):
            if level[y][x] > 899 and level[y][x] <= 999:
                doors.append(Door([x, y]))
    return doors

def openDoor(doors, coords, frameCount):
    for door in doors:
        distToDoor = math.sqrt(pow(coords[0] - door.coords[0] - 0.5, 2) + pow(coords[1] - door.coords[1] - 0.5, 2))
        if distToDoor < 1:
            door.activate(frameCount)

class Door:
    def __init__(self, coords):
        self.coords = coords
        self.x, self.y = coords[0], coords[1]
        
        self.isOpen = False

        self.lastOpenedFrame = -64

        #1 = closed, 0 = open, in between is partially open
        self.velocity = 0

        self.offset = 0

    def activate(self, frameCount):
        if frameCount >= self.lastOpenedFrame + 64:
            self.lastOpenedFrame = frameCount
            if self.isOpen:
                self.isOpen = False
                self.velocity = 0.25 / 16
            else:
                self.velocity = -0.25 / 16
        else:
            return

    def update(self):
        self.offset += self.velocity
        if self.offset >= 0 and self.velocity > 0:
            self.velocity = 0
        elif self.offset <= -1 and self.velocity < 0:
            self.velocity = 0
            self.isOpen = True