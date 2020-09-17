// testing to see if we can send 16bit information across BTserial

#include "BluetoothSerial.h"        // include bluetoothserial package from ESP

char *pin = "1234";                 // set the pin code for bluetooth
BluetoothSerial SerialBT;           // constructer for a bluetooth serial object

int x = 0;
int y = 1;
int z = 2;
uint16_t i = 523;
bool go;


void setup() {
  // now we set up the bluetooth communication
  SerialBT.setPin(pin);             // set the pin code for bluetooth
  SerialBT.begin("ESP32test");      // begin bluetooth communication and set the bluetooth name

  Serial.begin(115200);             // start serial connection for debugging purposes

  // now we are are reaady to connect to the ESP32 via bluetooth
}


void Send16BitNumber(uint16_t num, char axis='e') {
  // I had an error here for the longest time because I made a int16_t instead of uint16_t
  uint16_t prefix;
  switch (axis) {
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

  Serial.print("num: ");
  Serial.print(num);
  Serial.print(" - ");
  Serial.print(num, BIN);
  num = num >> 2;
  Serial.print(" - ");
  Serial.println(num, BIN);

  Serial.print("prefix: ");
  Serial.print(prefix, BIN);
  prefix = prefix << 14;
  Serial.print(" - ");
  Serial.println(prefix, BIN);

  Serial.print("num again: ");
  num = num | prefix;
  Serial.println(num, BIN);

  Serial.println("");

  // seems like I cant send a 16bit number over serial, rather only one byte at a time
  // actually it only sends over the last byte of the number so
  //    255 = 11111111          => 11111111
  //    256 = 00000001 00000000 => 00000000

  // https://arduino.stackexchange.com/questions/58325/how-to-package-a-16-bit-integer-to-send-it-with-serial-write
  // so we should first send the MSM of the number
  // link should explain the bitwise operations
  SerialBT.write((num>>8) & 0xFF);
  // then the whole number, since it will only send the last byte that's already the LSbyte
  SerialBT.write(num & 0xFF);


//  lower_num = num >> 2;
//  new_prefix = prefix << 14;
//  final_num = lower_num | new_prefix;
//  SerialBT.write(final_num);

//  Serial.print("num: ");
//  Serial.println(num, BIN);
//  Serial.print("lower_num: ");
//  Serial.println(lower_num, BIN);
//  Serial.print("prefix
}


void loop() {
  if (SerialBT.available()) {
    switch (SerialBT.read()) {

      case '1':
        go = true;
        break;

      case '0':
        go = false;
        break;

      default:
        break;
    }
  }
  if (go) {
      Send16BitNumber(i, 'x');
      Send16BitNumber(i, 'y');
      Send16BitNumber(i, 'z');
      Send16BitNumber(i);
//  SerialBT.write(256);
//      Send16BitNumber(i, 'x');
//      Send16BitNumber(i, 'y');
//      Send16BitNumber(i, 'z');
//      Send16BitNumber(i);
//
      i ++; 
  }
  delay(20);
}
