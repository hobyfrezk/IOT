import httplib, urllib
 
# field1: user attendence, field2: led working state 5 states in total
 
def update(datatype, data):
    if datatype == "USER":
        params = urllib.urlencode({'field1': data, 'key':'NXCLG7W3AQVRDBL1'})
        print data
     
    if datatype == "LED":
        params = urllib.urlencode({'field2': data, 'key':'NXCLG7W3AQVRDBL1'})
        print data
         
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
     
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    conn.request("POST", "/update", params, headers)
    response = conn.getresponse()
    #print response.status, response.reason
    data = response.read()
    conn.close()
