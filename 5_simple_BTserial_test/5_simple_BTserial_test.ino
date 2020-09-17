// simple sketch for sending serial data over bluetooth

#include "BluetoothSerial.h"        // include bluetoothserial package from ESP

char *pin = "1234";                 // set the pin code for bluetooth
BluetoothSerial SerialBT;           // constructer for a bluetooth serial object


void setup() {
  // now we set up the bluetooth communication
  SerialBT.setPin(pin);             // set the pin code for bluetooth
  SerialBT.begin("ESP32test");      // begin bluetooth communication and set the bluetooth name

  Serial.begin(115200);             // start serial connection for debugging purposes

  // now we are are reaady to connect to the ESP32 via bluetooth
}

char i;
char j;
bool iterate;


void loop() {
  if (SerialBT.available()) {
    switch (SerialBT.read()) {
      case '1':
        iterate = true;
        break;
      default:
        iterate = false;
        break;
    }
  }
  if (iterate) {
    SerialBT.write('x');
    SerialBT.write(i);
    SerialBT.write(j);
    if (j == 255) {
      i ++;
    }
    j ++; 
    Serial.print(i);
    Serial.println(j);
    delay(1);
  }
}
