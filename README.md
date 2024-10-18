# pycast-game
Raycasting engine written in Python with the Pygame library.

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
