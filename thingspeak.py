from lightsensor import Light
import httplib, urllib

# field1: user attendence, field2: lightsensor, field3: led working state

def update(datatype, data):
    if datatype == USER:
        params = urllib.urlencode({'field1': data, 'key':'NXCLG7W3AQVRDBL1'})
        
    if datatype == NATURALLIGHT:
        params = urllib.urlencode({'field2': data, 'key':'NXCLG7W3AQVRDBL1'})
    
    if datatype == LED:
        params = urllib.urlencode({'field3': data, 'key':'NXCLG7W3AQVRDBL1'})
        
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    conn.request("POST", "/update", params, headers)
    response = conn.getresponse()
    print response.status, response.reason
    data = response.read()
    conn.close()
