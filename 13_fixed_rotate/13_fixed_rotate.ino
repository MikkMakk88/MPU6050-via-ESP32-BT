#include "BluetoothSerial.h"        // include bluetoothserial package from ESP
#include <Wire.h>

const int MPU_addr = 0x68;
#define I2C_SDA 27
#define I2C_SCL 26
int16_t GyX, GyY, GyZ;              // using signed int for now, since readings are signed. This will changed when we use bit logic
char *pin = "1234";                 // set the pin code for bluetooth
BluetoothSerial SerialBT;           // constructer for a bluetooth serial object


void setup() {
  // first we want to initialize I2C communication with the module
  Wire.begin(I2C_SDA, I2C_SCL);
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);
  
  // now we set up the bluetooth communication
  SerialBT.setPin(pin);             // set the pin code for bluetooth
  SerialBT.begin("ESP32test");      // begin bluetooth communication and set the bluetooth name

  Serial.begin(115200);             // start serial connection for debugging purposes

  // now we are are reaady to connect to the ESP32 via bluetooth
}


void loop() {
  // allows the python script to control the ESP32
  if (SerialBT.available()) {
    switch (SerialBT.read()) {
      // send the 6 bytes of data when python sends a 1
      case '1':
        Wire.beginTransmission(MPU_addr);
        Wire.write(0x3B);
        Wire.endTransmission(false);
        Wire.requestFrom(MPU_addr, 6, true);
        for (int i=0; i<6; i++) {
          byte n = Wire.read();
          Serial.println(n);
          SerialBT.write(n);
        }
        Serial.println("");
        break;
        
      default:
        break;
    } 
  }
  delay(1);
}
