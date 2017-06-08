import time


def auto_mode(natural_light, pir_time):
    # if we use real light sensor:
    # # [
    # #   ...
    # #   state, (low_bound, up_bound)
    # #   ...
    # # ]
    # control_table = [
    #     ('0', (0, 100)),
    #     ('1', (101, 800)),
    #     ('2', (801, 1500)),
    #     ('3', (1501, 3000)),
    #     ('4', (3001, 99999)),
    # ]

    # check if user presence:
    time_difference = time.time() - pir_time
    if time_difference < 900:
        presence = 1
    else:
        presence = 0

    if presence:
        # if we use real light sensor:
        # for state, (low_bound, up_bound) in control_table:
        #     if low_bound <= natural_light <= up_bound:
        #         return state
        return str(natural_light)
    else:
        return str(0)


def manual_mode(value):
    return value


def control(led, topic, data):
    if 'lux' in topic:
        led.set_surrounding_light(data['lux'])
        if led.mode == 'AUTO':
            led.set_state(auto_mode(led.surrounding_light, led.pir_time))

    elif 'switch' in topic:
        if str(data['switch']) in str(range(5)):
            led.set_mode('MANUAL')
            led.set_state(data['switch'])
        else:
            led.set_mode("AUTO")
            led.set_state(auto_mode(led.surrounding_light, led.pir_time))

    elif 'pir' in topic:
        if data['pir']:
            led.set_pir_time(data['timestamp'])
