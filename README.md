# IoT Assignment

Autonomous LED system 

1. what: 

    - The system is develped for office useage, we try to provide "smart" function, making deskmans to  have a better light working environment and with minimum distraction from it.

2. why:

    - Increase labour work effenciency
    - create a better working environment
    - Electricity reduction

3. how: 

    - The system can automatically control the inside led brightness according to natural light it sensed, no human interference needed. But if the user want, of course, he/she can control the light by him/herself. 
    - The system also provide auto switch-on/off based on the user attendance.


The whole project is made up of several parts:

1. Hardware part
    - Respberry:
        - natural light sensor: Give response to natural light brightness.
        - motion sensor: Give response if the user is presense or not (simulated by a switch in this project).
        - switch: Switch to manual control mode.

2. Software part
    - MQTT:
        - Sensor publisher: Update sensor's data to broker
        - Broker: despatch received data 
        - Subscriber: Read data from broker and log to local
    - Control:
        - Main control script: read local data and make decision every 3 seconds.


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


1. Run 3 publishers scripts and subscriber script.
2. Run main server.
3. The system would set up with automode by default. The user can switch to interactive by press mode control button on the breadboard.
4. The user behavior and led working state will be transmitted to thingspeak channel as long as there is internet connection automatically, for further work attendance analysis and electricty control.
    - User behavior includes: user absence/presence
    - Led working state uncludes: 4 brightness of LED and if LED is turned off.





