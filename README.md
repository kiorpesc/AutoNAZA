AutoNAZA - beaglebone
========

Using a BeagleBone Black's PWM output with the DJI NAZA flight controller to implement modular autopilot.

DO NOT USE THIS YET.  It is still in very early testing,
and trying to use it will likely result in any one of numerous dangerous situations.
Your multirotor might fly off and never return.
It might also come straight for you with its propellers going at full throttle.
Or it might just slam itself into nearby obstacles.

DO NOT USE THIS CODE... at least until it has been thoroughly tested.


First steps:
============

DONE 1 - Control all NAZA inputs with BeagleBone's PWM outputs.

      -Uses modified Adafruit-BBIO library - branch is available as one of my repositories.
      
DONE 2 - Introduce pyGame to allow joystick control, test and tweak max values

      -Joystick control works, scaled to < half sensitivity, dead zone to help prevent accidental input to other axes

DONE 3 - Control data can be sent via cellular data link to anywhere in the country with minimal (read:acceptable) delay

      -Sends via TCP sockets, will try UDP as an alternative.

4 - GPS location and compass heading - need external hardware (GPS, magnetometer)

5 - Autonavigation - this includes waypoints, heading correction, ability to set speed, loiter at a waypoint

      -Position hold relying on GPS only will be innacurate
      -Altitude?

6 - Auto takeoff and landing

POC 7 - Video recording/streaming via wifi or cellular link

      -GStreamer coupled with a webcam with hardware h264 encoding provides a stable and low-latency stream

8 - Implement MAVLink commands for the system to make it work with existing ground control programs
