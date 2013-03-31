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
// min ~ 1050 us, max ~ 1950 us

// Common servo setup values
int minPulse = 1050;   // minimum servo position, us (microseconds)
int maxPulse = 1950;  // maximum servo position, us



// User input for servo and position
int userInput[3];    // raw input from serial buffer, 3 bytes
int startbyte;       // start byte, begin reading input
int servo;           // which servo to pulse?
int pos[6];
int adjust[6];        //might be used for manual calibration
int i;               // iterator

int userPos;
unsigned long lastTime;    //increments at every read in which there is not enough data

void setup() 
{    
  //set controls to center
  for(i = 0; i < 6; i++){
    pos[i] = 1500;
  }
  //set throttle to 0
  pos[3] = 1950;
  //set gear switch to Attitude mode
  pos[5] = 1525;
  
  delay(5000);
  
  // Attach each Servo object to a digital pin
  //aileron should be 3 on UNO, 4 on micro
  aileron.attach(3);
  elevator.attach(5);
  throttle.attach(6);
  rudder.attach(9);
  gear.attach(10);
  
  // TO ADD SERVOS:
  //   servo5.attach(YOUR_PIN, minPulse, maxPulse);
  //   etc...

  // LED on Pin 13 for digital on/off demo
  //pinMode(ledPin, OUTPUT);

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
      userPos = userInput[1];
      // Packet error checking and recovery
      if (userPos == 255) { servo = 255; }

      // Assign new position to appropriate servo
      // Change to assign to variables, need constant control input
      
      pos[servo] = map(userPos, 0, 180, minPulse, maxPulse);
      
    }
    //millis() is number of milliseconds since Arduino boot
    lastTime = millis();
  }
  
  //FAILSAFE -- NO SERIAL DATA FOR 2 SECONDS -- only happens if script crashes.
  //Need to reinitialize python script with set of safe values.
  if (millis() - lastTime > 2000) {
      pos[1] = map(90, 0, 180, minPulse, maxPulse); //lock X
      pos[2] = map(90, 0, 180, minPulse, maxPulse); //lock Y
      //swap 3 and 4 because of joystick axis order
      pos[4] = map(115, 0, 180, minPulse, maxPulse;	// lower throttle to bring craft down at non-catastrophic speed.
      pos[3] = map(90, 0, 180, minPulse, maxPulse);	// lock rudder
      pos[5] = map(95, 0, 180, minPulse, maxPulse); // stay in attitude mode
  } 
      aileron.writeMicroseconds(pos[1]);    // move servo1 to 'pos'
      elevator.writeMicroseconds(pos[2]);
      throttle.writeMicroseconds(pos[4]);	//
      rudder.writeMicroseconds(pos[3]);
      gear.writeMicroseconds(pos[5]);
}
