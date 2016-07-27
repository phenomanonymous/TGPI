# TGPI

Welcome to my game, I have no clue what to call it yet.  In the meantime, I've dubbed it "Test Grid, Please Ignore", or, TGPI.

This is a 2d platformer developed in python/pygame that I wrote as a challenge/project to teach myself python and make my first game.

Here's what you'll need to run the game:
* Python 2.7+ (If on windows, make sure to add python to your PATH)
* Pygame 1.9.2 (Run tgpi.py with sudo privileges the first time to install this automatically)
	
Please make sure to download the correct installer for your architecture and operating system.  
After this, you should already be all set to go.

The game creates its levels from the level# text files.  
If you would like to make your own level, please, feel free!  
I have provided "demo-level.txt" as a convenient empty bordered level for you to work with.  
However, there are no rules to the length or height of the level, so feel free to get crazy.  
There are many different kinds of blocks you can create based on specific characters.  
Which block each character corresponds to is detailed in "Level_Editor_Legend.txt".

The levels are loaded in sequential order (and the game currently crashes after running out of levels because I have not yet created an endgame function).  
Due to this, please make your new level 1 + the number of the highest existing level so there are no conflicts.  
Also, please make a new entry in "Level-Creator-List.txt" with the level you made and a distinctive name so I know who did it, I'd like to credit you if I use your work
