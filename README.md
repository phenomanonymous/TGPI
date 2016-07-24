IMPORTANT NOTE:
	THIS IS AN UNRELIABLE METHOD OF MAINTAINING WORKING CODE AMONG SEVERAL PARTIES
	AS ANYONE CAN EDIT ANY FILE AT ANYTIME, AND CONFLICTS WILL ARISE.
	PLEASE MAKE LOCAL COPIES TO USE FOR EDITING, THEN UPLOAD THEM TO THE DROPBOX FOLDER
	WHEN YOU ARE FINISHED.


Hi! Welcome to my game, I'm not sure what to fucking call it yet.

Here's what you'll need to run the game:
	1. Python 2.7.5+ (be aware that for Mac users, you are most like already installed with at least 2.7.5.   If you are not sure, type "python -V" into your terminal to see what you are running)
		https://www.python.org/ftp/python/2.7.8/python-2.7.8.msi
	2. Pygame 1.9.2
		Windows:
			http://pygame.org/ftp/pygame-1.9.2a0.win32-py2.7.msi
		Mac:
			http://www.pygame.org/ftp/pygame-1.9.2pre-py2.7-macosx10.7.mpkg.zip
	
Please make sure to download the correct installer for your architecture and operating system.
Simply click "next" through everything, all default settings are fine.
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
Lastly, please do not edit files other than your own.

Finally, you can start the game:
	On Windows:
		Simply double-click the tgpi.py file
	On Mac/Linux:
		execute "./tgpi.py" in the terminal in your local directory where this is saved