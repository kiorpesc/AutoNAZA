/*
 * ------------------------------
 *   MultipleSerialServoControl
 * ------------------------------
 *
 * Uses the Arduino Serial library
 *  (http://arduino.cc/en/Reference/Serial)
 * and the Arduino Servo library
 *  (http://arduino.cc/en/Reference/Servo)
 * to control multiple servos from a PC using a USB cable.
 *
 * Dependencies:
 *   Arduino 0017 or higher
 *     (http://www.arduino.cc/en/Main/Software)
 *   Python servo.py module
 *     (http://principialabs.com/arduino-python-4-axis-servo-control/)
 *
 * Created:  23 December 2009
 * Author:   Brian D. Wendt
 *   (http://principialabs.com/)
 * Version:  1.1
 * License:  GPLv3
 *   (http://www.fsf.org/licensing/)
 *
 * Modified: 19 March 2013
 * Author:   Charles Kiorpes
 *
 */

// Import the Arduino Servo library
#include <Servo.h> 

// Create a Servo object for each servo
Servo aileron;
Servo elevator;
Servo throttle;
Servo rudder;
Servo gear;
// TO ADD SERVOS:
//   Servo servo5;
//   etc...

//NAZA initial values (uncalibrated)
// min ~ 1100 us, max ~ 1950 us

// Common servo setup values
int minPulse = 1100;   // minimum servo position, us (microseconds)
int maxPulse = 1950;  // maximum servo position, us

// User input for servo and position
int userInput[3];    // raw input from serial buffer, 3 bytes
int startbyte;       // start byte, begin reading input
int servo;           // which servo to pulse?
int pos;             // servo angle 0-180
int i;               // iterator

void setup() 
{ 
  // Attach each Servo object to a digital pin
  aileron.attach(2, minPulse, maxPulse);
  elevator.attach(3, minPulse, maxPulse);
  throttle.attach(4, minPulse, maxPulse);
  rudder.attach(5, minPulse, maxPulse);
  gear.attach(6, minPulse, maxPulse);
  
  // TO ADD SERVOS:
  //   servo5.attach(YOUR_PIN, minPulse, maxPulse);
  //   etc...

  // LED on Pin 13 for digital on/off demo
  pinMode(ledPin, OUTPUT);

  // Open the serial connection, 9600 baud
  Serial.begin(9600);
} 

void loop() 
{ 
  // Wait for serial input (min 3 bytes in buffer)
  if (Serial.available() > 2) {
    // Read the first byte
    startbyte = Serial.read();
    // If it's really the startbyte (255) ...
    if (startbyte == 255) {
      // ... then get the next two bytes
      for (i=0;i<2;i++) {
        userInput[i] = Serial.read();
      }
      // First byte = servo to move?
      servo = userInput[0];
      // Second byte = which position?
      pos = userInput[1];
      // Packet error checking and recovery
      if (pos == 255) { servo = 255; }

      // Assign new position to appropriate servo
      switch (servo) {
        case 1:
          aileron.write(pos);    // move servo1 to 'pos'
          break;
        case 2:
          elevator.write(pos);
          break;
        case 3:
          throttle.write(pos);
          break;
        case 4:
          rudder.write(pos);
          break;
        case 5;
          gear.write(pos);

   // TO ADD SERVOS:
   //     case 5:
   //       servo5.write(pos);
   //       break;
   // etc...

        /* LED on Pin 13 for digital on/off demo
        case 99:
          if (pos == 180) {
            if (pinState == LOW) { pinState = HIGH; }
            else { pinState = LOW; }
          }
          if (pos == 0) {
            pinState = LOW;
          }
          digitalWrite(ledPin, pinState);
          break;
          */
      }
    }
  }
}
