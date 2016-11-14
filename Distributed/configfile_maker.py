
import json

config = {'mqtt': {'ip_address': '192.168.1.178'}, 
	  'thingspeak': {'thingspeak_key': 'NXCLG7W3AQVRDBL1'},
	  'mode': {'Automode': '0', 'Manualmode': '1'},
	  'zone': ['ZoneA', 'ZoneB', 'ZoneC'],
	  'device': {'led': ['led01', 'led02', 'led03', 'led04'],
		     'PIR': 'PIR01',
		     'Lightsensor': 'LSensor01'}
	 }


with open('config.json', 'w') as f:
    json.dump(config, f)
