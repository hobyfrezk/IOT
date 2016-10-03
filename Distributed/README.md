Led control Script

1. How does it work
  - define a working property which includes information about environment brightness, currrent working mode and current working state and user attendence time.
  - whenever receiving message from sensor, updating related states on that property and make a new command based on new working state.

2. call-back function for hearing from natural light sensor:

  (1) update natural brightness state
  
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

4. call-back function for hearing from control button:




THINGSPEAK 
