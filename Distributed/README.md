MQTT topics structures:

- /sensor/#
- /sensor/ZoneID/motion/#
- /sensor/ZoneID/motion/DeviceID/
- /sensor/ZoneID/light/
- /sensor/ZoneID/switchbutton/#
- /sensor/ZoneID/switchbutton/DeviceID/
- /led/#
- /led/ZoneID/#
- /led/ZoneID/DeviceID/#
- /led/ZoneID/DeviceID/WorkState/

payload structure:

- light: (string number), brightness of natural light
- motion: (time), time of motion detected
- button: ("Automode") or (string number from 1 to 5)


Led control Script

1. How does it work
  - define a working property which includes information about environment brightness, currrent working mode and current working state and user attendence time.
  - in total, a led subscribes message sent by devices in same zone, those devices include one light sensor which gives brightness of enviornment as a digit number, one motion sensor which send a time data when a user attendence detected, and one panel which used to switch working mode under user's will.
  - whenever receiving message from sensor, updating related states on that property and make a new command based on new working property.

2. call-back function for hearing from natural light sensor:

  (1) update enviornment brightness state
  
  (2) check working mode
    - if working mode == auto:
        - control led based on the natural brightness
        - renew working state 
    - if working mode == interactive mode:
        - do nothing
    
    
3. call-back function for hearing from PIR motion sensor:
  
  (1) update user attendence time 
  
  (2) check working mode
    - if working mode == auto (even if working state = 0 (which means the led is turned off)):
      - control led based on the natural brightness (which means, may turned on the led)
      - set working state
     - if working mode == interactive mode:
        - do nothing   

4. call-back function for hearing from control panel:

  (1) if payload == automode:
    - set led working mode = automode
    - set working state based on current property
    
  (2) if payload is a digit number(which means user wants access to interactive mode and give a command about willing led brightness):
    - set led working mode = interactivemode
    - set worlomg state based on user demand.

5. trigger function for sleep mode:
  - create a thread running in background
  - compare current time with last user detected time(which received from PIR) 
  - when the difference reaches 15 minutes 
  - check user absence probability, if the result tends to user absence then turn off led (working state = 0)
    


THINGSPEAK 














