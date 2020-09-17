// send data from MPU-6050 over BTserial
// each data chunk is 3 bytes: 1 byte for the axis and 2 bytes for the 16bit integer

#include "BluetoothSerial.h"        // include bluetoothserial package from ESP
#include <Wire.h>                   // include the I2C library

const int MPU_addr = 0x68;          // I2C address of the module
#define I2C_SDA 27                  // set the I2C communcation pins
#define I2C_SCL 26
int16_t GyX, GyY, GyZ;              // variables for gyroscope values (16but fixed length int)
char *pin = "1234";                 // set the pin code for bluetooth
BluetoothSerial SerialBT;           // constructer for a bluetooth serial object


void setup() {
  // first we want to initialize the I2C communication with the MPU-6050
  Wire.begin(I2C_SDA, I2C_SCL);
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);                 // still unsure what this does
  Wire.write(0);                    // write 0 to the device to wake it up
  Wire.endTransmission(true);
  
  // now we set up the bluetooth communication
  SerialBT.setPin(pin);             // set the pin code for bluetooth
  SerialBT.begin("ESP32test");      // begin bluetooth communication and set the bluetooth name

  Serial.begin(115200);             // start serial connection for debugging purposes

  // now we are are reaady to connect to the ESP32 via bluetooth
}


// false until python receiving byte from python script telling it to become true
// allows the python script to control whether the ESP should read from the MPU
bool conn;
char axis[3] = {'x', 'y', 'z'};     // set up chars for each axis


void loop() {  
  if (SerialBT.available()) {       // if receive 1 then start the loop, 0 stops the loop
    switch (SerialBT.read()) {
      case '1':
        conn = true;
        break;
      default:
        conn = false;
        break;
    }
  }
  if (conn) {
    Wire.beginTransmission(MPU_addr);
    Wire.write(0x43);                  // tell the MPU that we want to receive values from this address (0x43 = GYRO_XOUT_H)
    Wire.endTransmission(false);
    // request a total of 6 register from the MPU starting at register 0x43
    Wire.requestFrom(MPU_addr, 6, true);

    // The value of each axis is stored over 2 registers as a 16bit value.
    // we first send over a char byte to tell the python script which axis we are talking about
    // then we send over 2 bytes in sequence to communicate the whole 16bit integer
    for (int i=0; i<3; i++) {
      SerialBT.write(axis[i]);
      SerialBT.write(Wire.read());
      SerialBT.write(Wire.read());
    }
    delay(99);
  }
  delay(1);
}
