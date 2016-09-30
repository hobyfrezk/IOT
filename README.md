# IOT

Autonomous LED system 

1. what: 

    - The system is develped for office useage, we try to provide "smart" function, making deskmans to  have a better light working environment and with minimum distraction from it.

2. why:

    - Increase labour work effenciency
    - create a better working environment
    - Electricity reduction

3. how: 

    - The system can automatically control the inner led brightness according to natural light it sensed, no human interference needed. But if the user want, of course, he/she can control the light by him/herself. 
    - The system also provide auto switch-on/off based on the user attendance.
    
    
Main control work flow logic (pseudocode) and system introdction:

    while Ture:
        if mode = auto:
            if USERPRESENCE:
                adjustLED based on natural light
            elif USERABSENCE:
                if absenceTime > 15 mins
                    turnOffLED()
                if absenceTime < 15 mins
                    pass
        elif mode = manual:
            adjustLED based on user selection
            
            
As a distrubuted light control system

- Configuration:

- PIR motion sensor:

- Light sensor:

- Button:

- Led:

