Robots
======

This is my attempt at a robots game.

To run it, execute (make sure you have a large terminal window):

    python game.py

The robots run a program, stored in the "test.cpu" file. You can modify this 
program however you want. Only a few opcodes available right now.

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


