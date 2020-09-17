// testing to see if we can send 16bit information across BTserial

#include "BluetoothSerial.h"        // include bluetoothserial package from ESP
#include <Wire.h>

const int MPU_addr = 0x68;
#define I2C_SDA 27
#define I2C_SCL 26
int16_t GyX, GyY, GyZ;              // using signed int for now, since readings are signed. This will changed when we use bit logic
char *pin = "1234";                 // set the pin code for bluetooth
BluetoothSerial SerialBT;           // constructer for a bluetooth serial object
bool conn;
char axes[3] = {'x', 'y', 'z'};

#define dScale 1


void Send16BitNumber(uint16_t num, char axis='e') {
  // this function takes in a 16bit integer value and an axis, encodes the data,
  // and then sends it over BTserial
  
  uint16_t prefix;                // I had an error here for the longest time because I made a int16_t instead of uint16_t
  switch (axis) {                 // assign a value to variable prefix based on given axis char
    case 'x':
      prefix = 0;
      break;
    case 'y':
      prefix = 1;
      break;
    case 'z':
      prefix = 2;
      break;
    case 'e':    // error
      prefix = 3;
      break;
  }
  num = num >> 2;                       // bitshift to the right and truncate the 2 most LSB
  prefix = prefix << 14;                // bitshift the prefix to the left
  num = num | prefix;                   // bitwise or them together
  
  //    now the reading from the gyro is effectively a 14 bit number with a 2 bit prefix
  //    prefix(len2)    value(len14)
  //    V               V
  //    01              000000 00000000  
  //    We DO lose a tiny bit of precision this way, but the value will only ever be off by 3 at most and that
  //    is not nearly enough to matter

  // now we need to transmit the number 1 by at a time. Attempting to write data that is more than 1 byte will
  // only write the LSB. Thus we do it this way:
  SerialBT.write((num>>8) & 0xFF);      // bitshift to send the MSB first
  SerialBT.write(num & 0xFF);           // then the LSB
}


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
  // allows the python script to control whether the ESP will loop or not
  if (SerialBT.available()) {
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
      Wire.write(0x43);
      Wire.endTransmission(false);
      Wire.requestFrom(MPU_addr, 6, true);

      for (int i=0; i<3; i++) {
        char axis = axes[i];
        byte MSB = Wire.read();
        byte LSB = Wire.read();
        uint16_t val = MSB << 8 | LSB;
        Serial.print("axis: ");
        Serial.print(axis);
        Serial.print(" - val: ");
        Serial.println(val);
        Send16BitNumber(val, axis);
      }
      Serial.println("");
      delay(20 * dScale);
  }
  delay(1 * dScale);
}
