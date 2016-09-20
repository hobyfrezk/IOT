# IoT Assignment

Introduction

1. what: 

    - The system is develped for office useage, we provide "smart" function to make deskman have better light environment with minimum distraction from it.

2. why:

    - increase labour work effenciency
    - create a better working environment
    - electricity reduction

3. how: 

    - the system can automatically control the inside led brightness according to natural light it sensed, no human interference needed. But if the user want, of course, he/she can control the light by him/herself. 
    - the system also provide auto switch-on/off based on the user attendance.


The whole project is made up of several parts:

1. hardware part
    - Respberry:
        - natural light sensor: Give response to natural light brightness.
        - motion sensor: Give response if the user is presense or not (simulated by a switch in this project).
        - switch: Switch to manual control mode.

2. software part
    - MQTT:
        - Sensor publisher: Update sensor's data to broker
        - Broker: despatch received data 
        - Subscriber: Read data from broker and log to local
    - Control:
        - Main control script: read local data and make decision every 3 seconds.


Work flow logic (pseudocode):

    while Ture:
        if mode = auto:
            if USERPRESENCE:
                adjustLED("natural light")
            elif USERABSENCE:
                if absenceTime > 15 mins
                    turnOffLED()
                if absenceTime < 15 mins
                    pass
        elif mode = manual:
            adjustLED("user demand")



