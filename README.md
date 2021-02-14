# mpk249
The MPK249 is a beautiful machine, but it sucks to use with Ableton.

Ableton scripting sucks, remotify.io really sucks and is expensive.

Don't you just want a free, easy way to make ableton behaviors light up your MPK249 the right way?
You assign a pad to a binary ableton feautre, and it just works and changes color when the thing you mapped it to changes.

Of course you want this. Here it is.

# Installation
pip install rtmidi

Run the script.

# TODO
Hook this and rtmidi copy into ableton 

# How does it work
This script creates a virtual midi port, and sits in the middle. It retimes messages from Ableton so that pad light signals on the MPK249 come after the pad is depressed.

It can do more cool stuff too later. 
