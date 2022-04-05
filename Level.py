class Level:
    def __init__(self, floor_map, wall_map, ceiling_map):
        self.setWallMap(wall_map)
        self.setFloorMap(floor_map)
        self.setCeilingMap(ceiling_map)
    def setWallMap(self, new_map):
        self.wall_map = new_map
    def setFloorMap(self, new_map):
        self.floor_map = new_map
    def setCeilingMap(self, new_map):
        self.ceiling_map = new_map
    def getWallMap(self):
        return self.wall_map
    def getFloorMap(self):
        return self.floor_map
    def getCeilingMap(self):
        return self.ceiling_map