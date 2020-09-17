// simple initial sketch to send MPU6050 values via bluetooth

#include "BluetoothSerial.h"        // include bluetoothserial package from ESP
#include <Wire.h>                   // include I2C library

const int MPU_addr = 0x68;          // I2C address of GY-521
const int I2C_SDA = 27;                 // set the I2C communication pins
const int I2C_SCL = 26;
int16_t GyX, GyY, GyZ;              // pointers for gyroscope values (16bit fixed length int)
char *pin = "1234";                 // set the pin code for bluetooth
BluetoothSerial SerialBT;           // constructer for a bluetooth serial object


void setup() {
  // firstly lets initialize the I2C communication with the MPU-6050
  Wire.begin(I2C_SDA, I2C_SCL);     // initialize I2C 
  Wire.beginTransmission(MPU_addr); // Begin transmission to I2C slave
  Wire.write(0x6B);                 // unsure what this does still
  Wire.write(0);                    // write 0 to the device to wake it up
  Wire.endTransmission(true);       // unsure what this does also

  // now we set up the bluetooth communication
  SerialBT.setPin(pin);             // set the pin code for bluetooth
  SerialBT.begin("ESP32test");      // begin bluetooth communication and set the bluetooth name

  Serial.begin(115200);             // start serial connection for debugging purposes

  // now we are are reaady to connect to the ESP32 via bluetooth
}


void loop() {
  Wire.beginTransmission(MPU_addr); // begin transmission to I2C slave
  // starting with register 0x43 (GYRO_XOUT_H)
  Wire.write(0x43);
  Wire.endTransmission(false);      // I guess this tells the MPU we want to keep communcation open... not sure
  // request a total of 6 registers
//  Wire.requestFrom(MPU_addr, 6, true);
  Wire.requestFrom(MPU_addr, 2, true);

  int parta;
  int partb;
  parta = Wire.read();
  partb = Wire.read();

  SerialBT.write(parta);
  Serial.print(parta);
  SerialBT.write(partb);
  Serial.println(partb);

  // look at ESP32_gyro_test for explanation
//  GyX = Wire.read()<<8|Wire.read();
//  GyY = Wire.read()<<8|Wire.read();
//  GyZ = Wire.read()<<8|Wire.read();

  // for now we can send serial data over like this, it might make sense to do some smart bitwise stuff in the future
  // dunno, depends on speed
//  SerialBT.write('x');
//  SerialBT.write(GyX);
//  Serial.println(GyX);
  
//  SerialBT.write('y');
//  SerialBT.write(GyY);

//  SerialBT.write('z');
//  SerialBT.write(GyZ);

  delay(2500);
}
