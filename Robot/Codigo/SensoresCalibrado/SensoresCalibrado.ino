/*
Code to control a HC-SR04 with an Arduino Uno R3
It is little simplification of Ultrasonic.cpp - Library for HC-SR04 Ultrasonic Ranging Module.library
Created by ITead studio. Apr 20, 2010. iteadstudio.com
Modificated by Xarpe Serpe  
*/

const int trig0 = A0; // Pin trigger.
const int echo0 = A1; // Pin echo.
const int trig1 = A2;
const int echo1 = A3;

void setup() 
{ 
   
  Serial.begin(9600); // initialize serial communication:
  pinMode(trig0, OUTPUT);
  pinMode(echo0, INPUT);
  pinMode(trig1, OUTPUT);
  pinMode(echo1, INPUT);
  while (!Serial); 			// espera a enumeracion en caso de modelos con USB nativo
  Serial.println(F("Inicio:"));		// muestra texto estatico
  Serial.println(F("Presionar cualquier tecla y ENTER"));
  while (Serial.available() && Serial.read());		// lectura de monitor serie
  while (!Serial.available());   			// si no hay espera              
  while (Serial.available() && Serial.read()); 		// lecyura de monitor serie
} 
  
void loop() 
{ 
  makePingIzq(); //Send a sonic burst and measure the time to echo, them calculate the distance.
    delay(200);
  makePingDer();
    delay(200);
} 

void makePingIzq()
{
// establish variables for duration of the ping, 
// and the distance result in inches and centimeters:
long duration, cm;

  // The PING))) is triggered by a HIGH pulse of 2 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  digitalWrite(trig0, LOW);
  delayMicroseconds(2);
  digitalWrite(trig0, HIGH);
  delayMicroseconds(10); // The sonics burst has 0.340 cm of length.
  digitalWrite(trig0, LOW);

  // A HIGH pulse whose duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  duration = pulseIn(echo0, HIGH);

  // convert the time into a distance

  cm = microsecondsToCentimeters(duration);
  Serial.print(cm);
  Serial.print("cm");
}

void makePingDer()
{
// establish variables for duration of the ping, 
// and the distance result in inches and centimeters:
long duration, cm;

  // The PING))) is triggered by a HIGH pulse of 2 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  digitalWrite(trig1, LOW);
  delayMicroseconds(2);
  digitalWrite(trig1, HIGH);
  delayMicroseconds(10); // The sonics burst has 0.340 cm of length.
  digitalWrite(trig1, LOW);

  // A HIGH pulse whose duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  duration = pulseIn(echo1, HIGH);

  // convert the time into a distance

  cm = microsecondsToCentimeters(duration);
  Serial.print(cm);
  Serial.print("cm");
  Serial.println();

}

long microsecondsToCentimeters(long microseconds)
{
  // The speed of sound is 340 m/s or 29.4117647 microseconds per centimeter.
  // The ping travels out and back, so to find the distance of the
  // object we take half of the distance travelled.
  
  //return (microseconds / 29.4117647 / 2.); // without calibration.
  
  return (microseconds / 29.4117647 / 2.-1.511372549019610)/0.908687782805430;
  
  // The last two numbers came from the calibration of my own HC-SR04 module
  // For make that, you need to make a linear regression with real measurement
  // and the measuremente gived by the program.
}



