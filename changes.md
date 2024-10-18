
## Changelog
### 5/13/22
+Fixed bugs  
+Changed system for loading levels, cutting reliance on LevelData.py and Map.py  
+Added hallway mapping to assist enemy pathfinding  
+Added HIRs mapping, creating a graph of the map to aid in pathfinding speed  
+Added AI pathfinding  
+Added weapons for AI enemies  
+Added doors w/ opening/closing animations  
+Cleaned up file structure  
+Animated enemies  
+Added support for a configuration file  
+Upgraded minimap to show more detail  
+Added a red marker showing the spawn location of the player in the level editor  
+Added ability to easily change the spawn location in level editor by pressing 'u'  
+Added ability to remove any NPC from level editor  
+Added sounds for doors, guns, and pickups  
+Added textured floors & ceilings   
+Added dynamic resolution scaling  
+Added menu
### 1/19/22
+Optimized LevelCreator.py  
+Added fullscreen support(fullscreen option in Render.py)  
+Greatly optimized rendering speed  
+Implemented weapon system  
+Implemented health system  
+Implemented UI showcasing relevant info to player  
+Changed file structure of "assets" folder  
+Implemented "ghost" assets that have been unused thus far  
### 12/19/21
+New object rendering system resulting in major performance uplift.  
+Added support for live map updates with ability to save and export.  
+Bug fixes.  
### 12/6/21
+Added LevelCreator.py, the in game level editor  
+Support for in game level editor/creator  
+GUI for saving/loading/exporting files in level creator  
+GUI for changing block ID within level editor  
+Improved upon collision detection for NPC's  
+Implemented collision detection for objects  
+Added Sprites.py, a universal sprite container  
-Depracated MapGen.py, this utility functioned outside of the build of the engine and has bee replaced by the in game level editor 
### 12/1/21
Initial Commit

# Changes
Below is a list of changes I intend to make, as of now, this is **all** that will be done before this project is considered "complete" and is to serve as a checklist.  This, of course, is tentative.  This list will be done mostly in order from top to bottom, starting with all of the intended technical changes.

## TODO
Listed in order of current priority
###### 0% -Add support for multiple levels
###### 0% -Add support for custom NPC pathfinding
###### 0% -Add support for using the map builder standalone
###### 0% -(Maybe?) Build a UI for building elements, not just relying on editing configuration files
###### 0% -Move performance critical code to C++(rendering, pathfinding)
###### 50% -Add support for menus