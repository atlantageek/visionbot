
![alt tag](https://raw.github.com/atlantageek/visionbot/master/visionbot.jpg)
[[https://github.com/atlantageek/visionbot/master/visionbot.jpg|alt=octocat]]

This is the code for the maze solving robot using computer vision.  (put cute acronym here)

take_panorama.py - The python code that takes multiple images using a camera mounted on a servo.  Works with arduino

(Put fritzing here)

build_panorama.cpp - The cpp code that generates the panorama from three images.  compile it like so.

g++ -Wall build_panorama.cpp -I `pkg-config --libs --cflags opencv` -o build_panorama

process_maze.py - The python code that will solve the maze.

mazex.py - An attempt of maze solving with computer vision.  The start and end points are hardcoded.
