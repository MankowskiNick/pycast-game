# pycast-game
Raycasting engine written in Python with the Pygame library.

## Changelog
###### 12/1 - Initial Commit

## Upcoming changes
###### 50% -Support for live map updates with ability to save and export. 
###### 0% -Object rendering optimization.
###### 10% -Implementation of a health system
###### 0% -Universal sprites across files

## Utilization of MapGen.py
Pycast comes with a map already patched in to the game, however, you can change this through a built in tool.  Currently this is a separate tool, entitled MapGen.py
### Opening MapGen.py
Running MapGen.py will prompt you to input the dimensions for a new, blank level in terminal.  Once this is completed, you will be able to access the rest of the functionality of MapGen.py
### Changing tile selection
By default, the tile assigned at dictionary value spriteList[1] is the tile you are placing using MapGen.py.  By pressing N, you will be prompted in terminal to type the ID of the new tile/object sprite you would like to place.  In order to successfully create a level, there must be at least one object/npc placed as well as one spot with a tile value of -1, this represents the starting position of the player.
### Saving levels
Saving levels using MapGen.py will write level information to levels/[filename].leveldata.  Upon saving, you will be prompted in terminal to include a file name that you would like to save to.  Saving a file does **NOT** patch it in to the engine and is intended only to store progress on a current level design.
### Opening levels
Opening levels using MapGen.py will import level information from levels/[filename].leveldata.  Upon opening, you will be promped in terminal to include a file name you would like to open.  If this file does not exist, the terminal will ask again for a new file name.
### Exporting levels
Exporting a saved .leveldata file will patch that level in to the game through the LevelData.py file included. Currently, live map editing is not available, however this is in the works.  MapGen.py is a separate tool from the engine itself and allows full customizable level creation.  In order to properly use the editing tool and patch levels in to the game, you **MUST** save the current map to a file and **THEN** it will allow you to patch saved files in to the engine.  You cannot patch unsaved levels in to the engine.

## Controls
### pycast-game
###### WASD - Movement
###### JL - Rotate camera
###### M - Enter map creation tool

### Map Creation Toolkit Controls
###### O - Open from file, will be prompted in terminal for file name.
###### S - Save to file, will be prompted in terminal for file name.
###### E - Export saved file to game. NOTE: Exporting unsaved levels is not currently supported.
###### N - Change tile value you are placing.
###### Left click - place tile at mouse position
###### Right click - remove tile at mouse position
