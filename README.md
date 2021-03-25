# ScooterHack
With this project I am trying to look for BLE default risks in rental kick-scooters.
The program developed send commands to e-scooters parked nearby over Bluetooth Low Energy for Linux systems.

Before using it:
- Be sure to use python3.
- You are required to have bluepy to run correctly.

Running the program:
The program will be taking two arguments:
1) The type of scan:
  - Can either be scan which scans all available devices or saved which scans all known devices saved in a file. If during a scan the program succesfully locates a scooter it will save its address in the known devices file.

2) Command to send to the scooter
  - Second argument can be one the following commands:
  lock - this locks the scooter.
  unlock - this unlocks the scooter.

*Root is required to run the progarm in order to gain access to the system's lower bluetooth functions.*

Example to run the program:
sudo python3 scooter-scan.py scan unlock
