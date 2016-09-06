Robots
======

This is my attempt at a robots game.

To run it, execute (make sure you have a large terminal window):

    python game.py

Now open a web-browser, and point it to http://localhost:8000. Click on "Reset 
Game", then "Add Player" a couple times. Hit the play button to start the game.

The "Player" robots are executing a program, coded in the "test"cpu" file. Its
a simple implementation of "left hand rule" for going through the maze. If it 
bumps into anything, the robot fires it's weapon.

The "Random Player" are randomly generated code for the robots to execute. Most
of the time, they dont do much. But once in a while you'll get a creative one.

The idea
--------

I wanted something where I could 'program' a robot to wander a maze, and 
eventually shoot enemies. I have cpu cycles implemented, but not used. I also 
want to implement memory limits, and real opcodes, so we can get some self 
modifying code in there too. Some sort of resource management would be fun too,
damage and repair, and so on. Tons of ways we can go with it.

Yeah. I know there's some levels of indirection that I probably don't need. But
I wanted 'replacable' CPUs, without having to re-write the game itself. As long
as we can hook up the IO, we can use whatever "CPU" we want. 

I'm also trying to figure out if I like the "WorldPlayerController" as the 
interface betweeen the player and the world. Its still seems messy to me.


