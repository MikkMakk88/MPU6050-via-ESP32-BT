// GPIO pins for I2C https://randomnerdtutorials.com/esp32-i2c-communication-arduino-ide/#:~:text=Connecting%20I2C%20Devices%20with%20ESP32,-I2C%20communication%20protocol&text=One%20is%20used%20for%20the,be%20pulled%20up%20with%20resistors.
// more info https://www.mschoeffler.de/2017/10/05/tutorial-how-to-use-the-gy-521-module-mpu-6050-breakout-board-with-the-arduino-uno/
// Based on the code from the elegoo kit

#include<Wire.h>                      // include I2C library
const int MPU_addr = 0x68;            // I2C address of the GY-521
int16_t AcX, AcY, AcZ, Tmp, GyX, GyY, GyZ;    // declare these pointers as 16bit fixed length integers

int I2C_SDA = 27;
int I2C_SCL = 26;

void setup() {
  // The default pins for I2C didn't work (GPIO33 and GPIO32), so we define our own instead
  Wire.begin(I2C_SDA, I2C_SCL);       // defining SDA and SCL pins: https://www.esp32.com/viewtopic.php?t=2058
  Wire.beginTransmission(MPU_addr);   // Begins a transmission to the I2C slave (GY-521 board)
  Wire.write(0x6B);                   // unsure what this does
  Wire.write(0);                      // set to 0 (wakes up the GY-521)
  Wire.endTransmission(true); 
  Serial.begin(57600);
}


void loop() {
  Wire.beginTransmission(MPU_addr);
  // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.write(0x3B);
  Wire.endTransmission(false);
  // request a total of 14 registers
  Wire.requestFrom(MPU_addr, 14, true);   

  // each register is an 8bit integer
  // first we read the first 8bit register and assign it to our 16bit variable
  // then we shift the bits to the left by 8
  // then we bitwise or the second 8bit register to the 8 remaining lsbits of the variable
  // repeat this for all variables
  AcX = Wire.read()<<8|Wire.read();   // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
  AcY = Wire.read()<<8|Wire.read();   // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  AcZ = Wire.read()<<8|Wire.read();   // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
  Tmp = Wire.read()<<8|Wire.read();   // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
  GyX = Wire.read()<<8|Wire.read();   // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  GyY = Wire.read()<<8|Wire.read();   // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  GyZ = Wire.read()<<8|Wire.read();   // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)

  Serial.print("AcX = "); Serial.print(AcX); 
  Serial.print(" | AcY = "); Serial.print(AcY); 
  Serial.print(" | AcZ = "); Serial.print(AcZ);
  //equation for temperature in degrees C from datasheet 
  Serial.print(" | Tmp = "); Serial.print(Tmp/340.00+36.53); 
  Serial.print(" | GyX = "); Serial.print(GyX);
  Serial.print(" | GyY = "); Serial.print(GyY); 
  Serial.print(" | GyZ = "); Serial.println(GyZ);

  delay(330);
}
