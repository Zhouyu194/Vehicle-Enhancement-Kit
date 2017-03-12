# Vehicle-Enhancement-Kit
## Overview
The goal of this project was to create a kit for older vehicles lacking safety certain features. These features include Parking Sensors, Blind Spot Sensors, Backup Camera, Alarm System, FM Transmitter, and Bluetooth Music. The motivation for this project is the number of accidents caused an unaware driving merging into another vehicle.
## Parts List
- Raspberry Pi 2 Model B+
- 9 x HR-SC04 Ultrasonic Sensors
- Raspberry Pi Camera Module v2
- Raspberry Pi 7" Touch Screen Display
- Bluetooth USB Module
- Elechouse FM Transmitter
- LightBlue Bean Microcontroller
- 3 x Shift Register(SN54HC595) 
- Various LEDs

## How to Connect the Hardware
### HR-SC04 Ultrasonic Sensors
The sensor numbering will be shown below. The Trigger Pin and Echo Pin Represent the Raspberry Pi GPIO Pin the sensor should be connected to.

| Sensor | Trigger Pin | Echo Pin |
| ------ | ----------- | -------- |
| 0 | 11 | 13 |
| 1 | 15 | 16 |
| 2 | 19 | 21 |
| 3 | 23 | 24 |
| 4 | 29 | 31 |
| 5 | 32 | 33 |
| 6 | 36 | 37 |
| 7 | 38 | 40 |

Sensor 0 - Driver Side Front

Sensor 1 - Front Center

Sensor 2 - Passenger Side Front

Sensor 3 - Passender Side Rear

Sensor 4 - Rear Center

Sensor 5 - Driver Side Rear

Sensor 6 - Driver Side Blindspot Sensor

Sensor 7 - Passenger Side Blindspot Sensor

### Shift Registers
SRCLK - Raspberry Pi Pin 7
RCLK - Raspberry Pi Pin 8
SER - Raspberry Pi Pin 10
SRCLR - Raspberry Pi Pin 12

The Shift Register output has the format

data[0] Object Detection for Left Blindspot Sensor

data[1] Object Detection for Right Blindspot Sensor

data[2:5] Magnitude of Distance for Sensor 5

data[6:8] Magnitude of Distance for Sensor 4

Etc


## Todo
- Create wireless Enable/Disable for Alarm System
- Bluetooth Music
