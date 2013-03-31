AutoNAZA
========

Using a Raspberry Pi and an Arduino Micro with the DJI NAZA flight controller to implement modular autopilot.

DO NOT USE THIS YET.  It is still in very early testing,
and trying to use it will likely result in any one of numerous dangerous situations.
Your multirotor might fly off and never return.
It might also come straight for you with its propellers going at full throttle.
Or it might just slam itself into nearby obstacles.

DO NOT USE THIS CODE... at least until it has been thoroughly tested.


First steps:
============

DONE 1 - Control all NAZA inputs with arduino and python (yes, python).

      -Using serial communications between python and arduino.
      
DONE 2 - Introduce pyGame to allow joystick control, test and tweak max values

      -Joystick control works, scaled to < half sensitivity, dead zone to help prevent accidental input to other axes

DONE 3 - Control data can be sent via cellular data link to anywhere in the country with minimal (read:acceptable) delay

      -Scripts still need better error handling in case of socket failure.

4 - GPS location and compass heading

5 - Autonavigation - this includes waypoints, heading correction, ability to set speed, loiter at a waypoint

6 - Auto takeoff and landing

7 - Video recording/streaming via wifi link
