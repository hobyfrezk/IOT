import json

mqtt = {'ip_address': '192.168.1.178', 
		'topicname': }

config = {'key1': 'value1', 'key2': 'value2'}

with open('config.json', 'w') as f:
    json.dump(config, f)
