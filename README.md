# pycast-game
Raycasting engine written in Python with the Pygame library.

## Project revival
2/13/22 - Today I have spent some time looking through the codebase of this project and have decided to revive it.  The documentation has been updated to include the new, previously undocumented features, as well as the upcoming changes.  The goal of this project is to build a functional and performant raycasting engine that could be used to build a retro fps game complete with a variety of assets, weapons, NPCs, and levels.

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

# How to use PyCast
## Utilization of the in engine level editor
Pycast comes with a map already patched in to the game, however, you can change this through a built in level editor.  To access the editor, simply press the m key while in game.  To exit the editor, press the q key while in the editor
### Changing tile selection
By default, the tile assigned at dictionary value spriteList[1] is the tile you are placing.  To change this value, press a number key that corresponds to the list of textures on the right hand side of the screen or click the mouse on the desired tile from the right hand menu of tiles.  A green box will highlight the currently selected tile value.
### Editing the ceiling/floor
Within the updated map editor, you are able to modify the texture of the floor/ceiling as well.  Utilizing the UI at the bottom of the map editor screen, you can toggle which sections are showing, as well as which section you are editing.  The selected options are highlighted in green.
### Saving levels
Saving levels using MapGen.py will write level information to levels/[filename].leveldata.  Upon saving, you will be prompted to include a file name that you would like to save to.  Saving a file does **NOT** permanently patch it in to the engine and is intended only to store progress on a current level design.
### Opening levels
Opening levels using MapGen.py will import level information from levels/[filename].leveldata.  Upon opening, you will be promped to include a file name you would like to open.  If this file does not exist, the request will be ignored.  

## Creating new assets with settings.conf
Creating new assets can be done very easily using the settings.conf file.  Utilizing this file, we can add new textures, add new NPCs, add new weapons, and add new pickups.
### Creating new wall/door textures
In order to create new wall textures, you simply need to put the corresponding sprite in the assets folder, likely in the 'walls' or 'doors' folders, depending on what you want it to be.  Once this is complete, you will pick an ID for the new asset, and simply add the ID with the path to settings.conf, under the [SPRITES] category.
### Creating new weapons
#### Configuring weapon sprites.
In order to create new weapons, there are a few more steps to be completed.  First off, you should have 4 sprites.  One of the weapon held still, and then 3 animation sprites(Examples of this can be found in assets/weapons/weapon_1/).  These sprites should be put in a folder inside the 'assets/weapons/' folder, this folder can be named whatever you would like, so long as it does not conflict with an already existing weapon. 
#### Configuring weapon behavior
Once you have the sprites in the correct folder, you can implement a new weapon by choosing a new weapon id.  Currently, a weapon id can be any integer 0-9 & will be accessed in game by pressing the corresponding number towards the top of the keyboard.  Once you have this picked, you must add a new entry under the [WEAPON_SPRITES] category in settings.conf.  This should be a list of the four sprites you had set up above, corresponding to the weapon id.  I recommend the format {weapon_name}_0.png - {weapon_name}_3.png, where {weapon_name}_0 is the static sprite and {weapon_name}_3 is the last animation sprite.  Once this is complete, you must also add an entry under the [WEAPONS] category in settings.conf.  This entry will also correspond to the weapon id you have picked and the information required is highlighted in more detail in settings.conf.

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
