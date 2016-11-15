
import json



config = {'mqtt': {'ip_address': '192.168.1.178'}, 
	  'thingspeak': {'thingspeak_key': 'NXCLG7W3AQVRDBL1'},
	  'mode_index': {'Automode': '0', 'Manualmode': '1'},
	  'sleep_timeout': '900' ,
	  'zone': [{'ZoneA': 'activated'}],
	  'device': {'LED': {'ZoneA': ['LED01']},
		     'PIR': {'ZoneA': ['PIR01']},
		     'Lightsensor': {'ZoneA': ['LSensor01']},
		     'button': {'ZoneA': ['button01']}
				 
	  'lamp_luminance': {'1000':'state1', '600': 'state2', '400':'state3', '100': 'state4'},
	  'lightsensor': {'address': '0x39','control_on': '0x03','control_off': '0x00'}
	 }

with open('config.json', 'w') as f:
    json.dump(config, f)
