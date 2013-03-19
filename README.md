AutoNAZA
========

Using a Raspberry Pi and an Arduino Micro with the DJI NAZA flight controller to implement modular autopilot.

There's not much here.

First steps:
============

1 - Control all NAZA inputs with arduino and python (yes, python).

      -Using serial communications between python and arduino.
      
2 - Introduce pyGame to allow joystick control, test and tweak max values

3 - Smooth transition from joystick control to tx/rx control in case of network failure

4 - GPS location and compass heading

5 - Autonavigation - this includes waypoints, heading correction, ability to set speed, loiter at a waypoint

6 - Auto takeoff and landing

7 - Video recording/streaming via wifi link
