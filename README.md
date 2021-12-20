# pycast-game
Raycasting engine written in Python with the Pygame library.

## Changelog
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

## Upcoming changes
###### 10% -Implementation of a health system.
###### 0% -Implement support for creation of new, empty levels.
###### 0% -Implement character drawing support for new levels on level editor
###### 0% -Create and implement additional textures, objects, and NPCs

## Utilization of the in game level editor
Pycast comes with a map already patched in to the game, however, you can change this through a built in level editor.  To access the editor, simply press the m key while in game.  To exit the editor, press the q key while in the editor
### Changing tile selection
By default, the tile assigned at dictionary value spriteList[1] is the tile you are placing.  To change this value, press a number key that corresponds to the list of textures on the right hand side of the screen.  A green box will highlight the currently selected tile value.
### Saving levels
Saving levels using MapGen.py will write level information to levels/[filename].leveldata.  Upon saving, you will be prompted to include a file name that you would like to save to.  Saving a file does **NOT** permanently patch it in to the engine and is intended only to store progress on a current level design.
### Opening levels
Opening levels using MapGen.py will import level information from levels/[filename].leveldata.  Upon opening, you will be promped to include a file name you would like to open.  If this file does not exist, the request will be ignored.
### Exporting levels
Exporting a saved .leveldata file will semi-permanently patch that level in to the game through the LevelData.py file included. The in game level editor, accessible by pressing the m key, allows full customizable level creation.  In order to properly use the editing tool and patch levels in to the game, you **MUST** save the current map to a file and **THEN** it will allow you to patch saved files in to the engine.  Editing maps in the editor will appear if you quit the editor and return to the game, however these edits will not appear once the engine is closed unless the level is saved and exported.

## Controls
### pycast-game
###### WASD - Movement
###### JL - Rotate camera
###### M - Enter map creation tool

### Map Creation Toolkit Controls
###### Q - Exit in game level editor
###### O - Open from file
###### S - Save to file
###### E - Export saved file to game. NOTE: Exporting unsaved levels is not currently supported.
###### Left click - place tile at mouse position
###### Right click - remove tile at mouse position
