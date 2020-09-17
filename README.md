### MPU6050 via ESP32 BT

This is a project I started to better learn how to use various tools.
Namely: 
1. the ESP32 microcontroller (especially its bluetooth functionality)
2. the MPU6050 gyroscope and accelerometer
3. OpenGL
4. interfacing with a midi instrument to use as an arbitrary controller

The ESP32 is hooped up to the MPU6050 and sends the sensor to the python script via bluetooth. This sensor data is then used to rotate a 3d shape made with OpenGL. I also experimented with using a midi controller to rotate the 3d object while I was still working on the ESP32 code.

Since I started this project without git the different stages are spread out over many folders marked in ascending order. This still seems quite useful however since there is still code in some of the older version that I would still like to reference. Therefor I'll keep the repo organised as is.