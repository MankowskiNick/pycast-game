# pycast-game
Raycasting engine written in Python with the Pygame library.

## Changelog
### 1/xx
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
### 1/19
+Optimized LevelCreator.py  
+Added fullscreen support(fullscreen option in Render.py)  
+Greatly optimized rendering speed  
+Implemented weapon system  
+Implemented health system  
+Implemented UI showcasing relevant info to player  
+Changed file structure of "assets" folder  
+Implemented "ghost" assets that have been unused thus far  
### 12/19
+New object rendering system resulting in major performance uplift.  
+Added support for live map updates with ability to save and export.  
+Bug fixes.  
### 12/6
+Added LevelCreator.py, the in game level editor  
+Support for in game level editor/creator  
+GUI for saving/loading/exporting files in level creator  
+GUI for changing block ID within level editor  
+Improved upon collision detection for NPC's  
+Implemented collision detection for objects  
+Added Sprites.py, a universal sprite container  
-Depracated MapGen.py, this utility functioned outside of the build of the engine and has bee replaced by the in game level editor 
### 12/1 
Initial Commit

# Changes
Below is a list of changes I intend to make, as of now, this is **all** that will be done before this project is considered "complete" and is to serve as a checklist.  This, of course, is tentative.  This list will be done mostly in order from top to bottom, starting with all of the intended technical changes.

## Upcoming technical changes
###### 0% -Add sound and music support
###### 0% -Add support for changing levels
###### 0% -Add support for menus
###### 0% -Add documentation for adding new things to engine(wall textures, objects, npcs, pickups, weapons)

## Upcoming creative changes
###### -Add more enemies
###### -Compose sounds and music
###### -Create more levels
###### -Create and stylize menus
###### -Come up with a name(?)

## Upcoming final changes prior to completion
###### -Finalize balancing mechanics
###### -Split game into release and development version(one with map editor, one without)

## Utilization of the in game level editor
Pycast comes with a map already patched in to the game, however, you can change this through a built in level editor.  To access the editor, simply press the m key while in game.  To exit the editor, press the q key while in the editor
### Changing tile selection
By default, the tile assigned at dictionary value spriteList[1] is the tile you are placing.  To change this value, press a number key that corresponds to the list of textures on the right hand side of the screen or click the mouse on the desired tile from the right hand menu of tiles.  A green box will highlight the currently selected tile value.
### Saving levels
Saving levels using MapGen.py will write level information to levels/[filename].leveldata.  Upon saving, you will be prompted to include a file name that you would like to save to.  Saving a file does **NOT** permanently patch it in to the engine and is intended only to store progress on a current level design.
### Opening levels
Opening levels using MapGen.py will import level information from levels/[filename].leveldata.  Upon opening, you will be promped to include a file name you would like to open.  If this file does not exist, the request will be ignored.  

## Controls
### pycast-game
###### WASD - Movement
###### JL - Rotate camera
###### M - Enter map creation tool

### Map Creation Toolkit Controls
###### Q - Exit in game level editor
###### O - Open from file
###### S - Save to file
###### Left click - place tile at mouse position
###### Right click - remove tile at mouse position
